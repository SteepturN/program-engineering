/*
https://en.wikipedia.org/wiki/Email

не понятно, зачем пользователь нужен, если это приложение как outlook
можно и нужно использовать разные аккаунты для компьютера
или просто разные компьютеры
если бы это был аккаунт...
видимо задание про собственный почтовый сервер, или онлайн почту, не приложение
хотя у outlook есть и приложение, и web-клиент

удивительно то, что отправлять сообщения не надо, только показывать их
и пользователями управлять, зачем тогда smtp & imap серверы нужны? по API больше
похоже на сервис для ведения заметок в облаке с их разделением по папкам,
а название Электронная почта
создано, чтобы запутать студента.

Приложение должно содержать следующие данные:
- почтовая папка
- сообщение
- пользователь
Реализовать API:
- Создание нового пользователя
- Поиск пользователя по логину
- Поиск пользователя по маске имя и фамилии
- Создание новой почтовой папки
- Получение перечня всех папок
- Создание нового письма в папке
- Получение всех писем в папке
- Получение письма по коду
*/
workspace "Outluck Email" {
    !identifiers hierarchical

    model {
        webApp = softwareSystem "Пользовательское приложение в браузере" {
            // there could be local folders on the PC,
            // but this would be a desktop app

            client = container "Client" "Receive and send API messages from web app" {
                technology "JavaScript+Fetch API+DOM"
            }
            app    = container "Application" {
                technology "JavaScript"
                createFolder            = component createFolder {
                    -> client "send request"
                }
                showAllFolders          = component showAllFolders {
                    -> client "send request"
                }
                writeMessageInFolder    = component writeMessageInFolder {
                    -> client "send request"
                }
                showAllMessagesInFolder = component showAllMessages {
                    -> client "send request"
                }
                addMessageToFolder      = component addMessageToFolder {
                    -> client "send request"
                }
            }
            editor = container "TextEditor" "Write messages" {
                technology "JavaScript+HTML+CSS+DOM+Fetch API"
                -> client "send written message"
            }
            gui    = container "Visual interface" {
                technology "CSS+HTML"
                -> app.showAllMessagesInFolder "check new messages"
                -> app.createFolder            "create folder"
                -> app.showAllFolders          "show all folders"
                -> app.writeMessageInFolder    "write message in folder"
                -> app.showAllMessagesInFolder "show all messages"
                -> app.addMessageToFolder      "add message to folder"
                -> editor                      "input stream"
            }
            client -> gui "draw update"
            editor -> gui "draw update"
        }
        emailSystem = softwareSystem "Электронная почта" {
            userDatabase     = container "Users database" {
                technology "PostgreSQL"
                tags "Database"
                createUser      = component "Создание нового пользователя"
                findUserByLogin = component "Поиск пользователя по логину"
                findUserByMask  = component "Поиск пользователя по маске имя и фамилии"
            }
            passwordDatabase = container "Passwords database" {
                technology "PostgreSQL"
                tags "Database"
                createUser      = component "Создание записи о хеше пароля нового пользователя"
                findUserByLogin = component "Поиск хеша пароля пользователя по логину"
            }
            folderDatabase   = container "Folders database" {
                technology "PostgreSQL"
                tags "Database"
                createFolder         = component "Создание папки"
                listFolders          = component "Список папок"
                listMessagesInFolder = component "Получение всех писем в папке"
                createMessage        = component "Создание нового письма"
                placeMessageInFolder = component "Размещение сообщения в папке"
            }
            messageDatabase  = container "Messages Database" {
                technology "PostgreSQL"
                tags "Database"
                getMessage    = component "Получение письма по коду"
                createMessage = component "Создание нового письма"
            }
            userService      = container "UserService"    "User search, creation" {
                technology "Python+FastApi"
                -> userDatabase.createUser              "Создание нового пользователя"
                -> passwordDatabase.createUser          "Создание нового пользователя"
                -> userDatabase.findUserByLogin         "Поиск пользователя по логину"
                -> userDatabase.findUserByMask          "Поиск пользователя по маске имя и фамилии"
            }
            authService      = container "AuthService"    "User authentication" {
                technology "Python+FastApi"
                -> passwordDatabase.findUserByLogin     "Аутентификация пользователя"
                -> webApp.client                        "sends token after authentication"
            }
            messageService   = container "MessageService" "Receive and send API messages" {
                technology "Python+FastApi"
                -> webApp.client                        "sends result request"

                -> folderDatabase.createFolder          "Создание папки"
                -> folderDatabase.listFolders           "Список папок"
                -> folderDatabase.listMessagesInFolder  "Получение всех писем в папке"
                -> folderDatabase.createMessage         "Создание нового письма"
                -> folderDatabase.placeMessageInFolder  "Размещение сообщения в папке"

                -> messageDatabase                      "get messages from ids"
                -> messageDatabase                      "create and store message"
            }
            folderDatabase -> messageService "ids & folders"
            messageDatabase -> messageService "messages"
            userDatabase -> userService "users"
            passwordDatabase -> authService "password hash"
        }
        user = person "Пользователь электронной почты" {
            -> webApp.gui "uses"
        }
        webApp.client -> emailSystem.authService     "sends token request"
        webApp.client -> emailSystem.messageService  "sends message requests"
        webApp.client -> emailSystem.userService     "sends user requests"
    }

    views {
        systemContext emailSystem {
            include *
            autolayout
        }
        container emailSystem {
            include *
            autolayout
        }

        systemContext webApp {
            include *
            autolayout
        }
        container webApp {
            include *
            autolayout
        }
        dynamic webApp.app "checkFolder" "authenticated user checks a folder" {
            1:  user                                            -> webApp.gui                                      "check new messages"
            2:  webApp.gui                                      -> webApp.app.showAllMessagesInFolder              "get all messages in the folder"
            3:  webApp.app.showAllMessagesInFolder              -> webApp.client                                   "send request"
            4:  webApp.client                                   -> emailSystem.messageService                      "send request to get all messages in a folder"
            5:  emailSystem.messageService                      -> emailSystem.folderDatabase.listMessagesInFolder "get ids of messages in a folder"
            6:  emailSystem.folderDatabase.listMessagesInFolder -> emailSystem.messageService                      "ids"
            7:  emailSystem.messageService                      -> emailSystem.messageDatabase                     "get messages from ids"
            8:  emailSystem.messageDatabase                     -> emailSystem.messageService                      "messages"
            9:  emailSystem.messageService                      -> webApp.client                                   "send messages for folder"
            10: webApp.client                                   -> webApp.gui                                      "update page with messages in the folder"
            11: webApp.gui                                      -> user                                            "show messages in the folder"

            autolayout
        }
        styles {
            element "Element" {
                background #009900
            }
            element "Person" {
                background #2D882D
                shape person
            }
            element "Software System" {
                background #2D882D
            }
            element "Container" {
                background #55aa55
            }
            element "Database" {
                shape cylinder
            }

        }
    }
}

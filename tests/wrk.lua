-- local frandom = io.open("/dev/urandom", "rb")
-- local d = frandom:read(4)
-- math.randomseed(d:byte(1) + (d:byte(2) * 256) + (d:byte(3) * 65536) + (d:byte(4) * 4294967296))

-- number =  math.random(1,100000)
request = function()
    headers = {}
    headers["Content-Type"] = "application/json"
    -- https://stackoverflow.com/questions/11068892/oauth-2-0-authorization-header
    headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VybmFtZVxuYWRtaW4iLCJleHAiOjE3NDU5NTE3Njd9.kVo5dZVxtMYJx-R5DRGtnE_J_RbqHeLf6Zm9nyfeB_w"
    body = ''
    -- return wrk.format("GET", "/users/".. tostring(number), headers, body)
    return wrk.format("GET", "/user/admin", headers, body)
end

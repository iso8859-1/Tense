-- basich logging infrastructure

-- log levels
LogLevels = { ERROR = 0, WARN = 1, INFO = 2, DEBUG = 3 }

Logger = { state = { loglevel = LogLevels.ERROR, broadcast = false} }

function Logger:loglevel()
    return self.state.loglevel
end

function Logger:error(msg)
    if self.loglevel(self) >= LogLevels.ERROR then
        env.error(msg)
        if (self.state.broadcast) then
            MESSAGE:New("ERROR: "..msg, 10):ToAll()
        end
    end
end

function Logger:warn(msg)
    if self.loglevel(self) >= LogLevels.WARN then
        env.warning(msg)
        if (self.state.broadcast) then
            MESSAGE:New("WARN: "..msg, 10):ToAll()
        end
    end
end

function Logger:info(msg)
    if self.loglevel(self) >= LogLevels.INFO then
        env.info(msg)
        if (self.state.broadcast) then
            MESSAGE:New("INFO: "..msg, 10):ToAll()
        end
    end
end

function Logger:debug(msg)
    if self.loglevel(self) >= LogLevels.DEBUG then
        env.info(msg)
        if (self.state.broadcast) then
            MESSAGE:New("DEBUG: "..msg, 10):ToAll()
        end
    end
end

function Logger:setLogLevel(level)
    Logger:info("Setting log level to " .. tostring(level))
    self.state.loglevel = level
end

function Logger:setBroadcast(broadcast)
    Logger:info("Setting broadcast to " .. tostring(broadcast))
    self.state.broadcast = broadcast
end

local function test()
    Logger:error("This is an error message")
    Logger:warn("This is a warning message")
    Logger:info("This is an info message")
    Logger:debug("This is a debug message")
end

local function init_logging_radio(menu)
    local MenuEnableBroadcast = MENU_MISSION_COMMAND:New("Enable Broadcast", menu, function() Logger:setBroadcast(true) end)
    local MenuDisableBroadcast = MENU_MISSION_COMMAND:New("Disable Broadcast", menu, function() Logger:setBroadcast(false) end)
    local MenuLogLevelError = MENU_MISSION_COMMAND:New("Log Level Error", menu, function() Logger:setLogLevel(LogLevels.ERROR) end)
    local MenuLogLevelWarn = MENU_MISSION_COMMAND:New("Log Level Warn", menu, function() Logger:setLogLevel(LogLevels.WARN) end)
    local MenuLogLevelInfo = MENU_MISSION_COMMAND:New("Log Level Info", menu, function() Logger:setLogLevel(LogLevels.INFO) end)
    local MenuLogLevelDebug = MENU_MISSION_COMMAND:New("Log Level Debug", menu, function() Logger:setLogLevel(LogLevels.DEBUG) end)
    local MenuTestLogging = MENU_MISSION_COMMAND:New("Test Logging", menu, function() test() end)
end

Logger_menu = MENU_MISSION:New("Logger")
init_logging_radio(Logger_menu)

Logger:info("Logger initialized")
-- Test Code
-- env.info("Test logging")
-- test()

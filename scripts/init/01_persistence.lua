-- functionality for persisting data between game sessions

PersistenceManager =
{
    objects = {}, -- object registry for objects to be persisted 
    scheduler = nil, -- scheduler for saving objects events
    dir = nil -- directory for saving objects
}

local JSON = (loadfile('Scripts/JSON.lua'))()

function PersistenceManager:init()
    -- create save file
    self.dir = lfs.writedir()..'Missions/Saves/'
    lfs.mkdir(self.dir)
    -- load objects
    self.load(self)
    -- create scheduler
    self.scheduler = SCHEDULER:New(nil, PersistenceManager.persist, {PersistenceManager}, 10, 60) -- save every 60 seconds
    local menuEnableBroadcast = MENU_MISSION_COMMAND:New("Force Persist", nil, function() PersistenceManager:persist() end)
end

function PersistenceManager:register(key, value)
    self.objects[key] = value
end

function PersistenceManager:retrieve(key)
    return self.objects[key]
end

function PersistenceManager:filename()
    return self.dir .. "persist.json"
end

function PersistenceManager:persist()
    local filename = self.filename(self)
    Logger:debug("Persisting objects to " .. filename)
    local json = JSON:encode(self.objects)
    local file = io.open(filename, "w")
    if not file then
        Logger:error("Could not open file for writing: " .. filename)
        return
    end
    file:write(json)
    file:close()
end

function PersistenceManager:load()
    local filename = self.filename(self)
    Logger:debug("Loading objects from " .. filename)
    local file = io.open(filename, "r")
    if not file then
        Logger:info("No persistence file found")
        return
    end
    local json = file:read("*a")
    file:close()
    self.objects = JSON:decode(json)
end

if lfs == nil then
    Logger:info("Mission running in sanatized environment. Persistence not available")
    return
end
PersistenceManager:init()
local logger_state = PersistenceManager:retrieve("logger")
if logger_state ~= nil then
    Logger:debug("Restoring logger state")
    Logger.state = logger_state
end
PersistenceManager:register("logger", Logger.state)
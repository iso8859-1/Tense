
local simulation = {
    zones = {}
}

local function findProperty(property_name, property_table)
    for _, value in pairs(property_table) do
        if value.key == property_name then
            return value.value
        end
    end
end

local function initSimulation()
    local zones = env.mission.triggers.zones
    for _, zone in pairs(zones) do
        Logger:debug("Zone: " .. zone.name)
        local type = findProperty("ZONE_TYPE", zone.properties)
        local tmp = {}
        tmp.type = type
        simulation.zones[zone.name] = tmp
    end
    -- local JSON = (loadfile('Scripts/JSON.lua'))()
    -- local json = JSON:encode(zones)
    -- local file = io.open("zones.json", "w")
    -- file:write(json)
    -- file:close()
end

local function getTableLength(table)
    local count = 0
    for _ in pairs(table) do count = count + 1 end
    return count
end

local function stateConsistencyCheck(state_zones)
    Logger:debug("Checking simulation state consistency")
    local mission_zones = env.mission.triggers.zones
    if getTableLength(mission_zones) ~= getTableLength(state_zones) then
        Logger:debug("Zone count mismatch.")
        return false
    end
    for _, value in pairs(mission_zones) do
        if state_zones[value.name] == nil then
            Logger:debug("Zone " .. value.name .. " not found in state")
            return false
        end
    end
    return true
end

local simulation_state = PersistenceManager:retrieve("simulation")
if simulation_state ~= nil then
    Logger:debug("Restoring simulation state")
    -- verify simulation state still valid
    if stateConsistencyCheck(simulation_state.zones) then
        Logger:info("Initializing simulation from save file")
        simulation = simulation_state
    else
        Logger:warn("Simulation state is not consistent with current mission. Reinitializing simulation")
        initSimulation()
    end
else
    Logger:info("Initializing simulation")
    initSimulation()
end
PersistenceManager:register("simulation", simulation)

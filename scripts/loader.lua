-- loads all script files in the init folder

function get_directory_from_path(path)
    return path:match("(.*[/\\])")
end

-- finds the path of the loader.lua file
-- as this may change for different developer PCs
function get_script_path()
    local str = debug.getinfo(get_script_path).source
    return get_directory_from_path(str)
end

-- loads all scripts in the init sub-folder
function load_init_scripts()
    local path = get_script_path() .. "init"
    env.info("Loading init scripts fom: " .. path)
    MESSAGE:New("Loading init scripts from " .. path, 10):ToAll()
    for file in lfs.dir(path) do
        if file ~= "." and file ~= ".." then
            local f = path..'/'..file
            if lfs.attributes(f, "mode") == "file" and f:match("%.lua$") then
                env.info("Loading script: " .. f)
                MESSAGE:New("Loading script: " .. f, 10):ToAll()
            end
        end
    end
end

-- check if the lfs module is available aka the mission is running in a sanitized environment or not.
if lfs == nil then
    env.warn("Mission running in sanatized environment.")
    MESSAGE:New("Mission running in sanatized environment. Not all features available", 10):ToAll()
    MESSAGE:New("To de-sanatize it, edit MissionScriptiong.lua", 10):ToAll()
    return
end
load_init_scripts()
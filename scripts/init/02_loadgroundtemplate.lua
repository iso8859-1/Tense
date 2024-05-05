local JSON = (loadfile('Scripts/JSON.lua'))()

function GetTemplatesPath()
	local path = GetScriptPath().."templates"
	return path
end

function LoadTempFile(filename)
	local filepath = GetTemplatesPath().."\\"..filename
	Logger:info("Start loading Template File" ..filepath)
	local readfile = io.open(filepath , "r")
	

	if readfile then
		local content = readfile:read("*a")
		readfile:close()
		local data  = JSON:decode(content)
		Logger:info("Template File loaded")
		return data
	else
		Logger:error("File not found")
	end
end

DataTemplate = LoadTempFile("GroundTroopsTemplate.json")







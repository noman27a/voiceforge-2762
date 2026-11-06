' VoiceForge 2762 — Windows launcher
' Starts the local server and opens the studio in the browser.
Option Explicit

Dim shell, fso, baseDir, pythonExe, url
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
baseDir = fso.GetParentFolderName(WScript.ScriptFullName)
pythonExe = fso.BuildPath(baseDir, ".venv\Scripts\pythonw.exe")
url = "http://127.0.0.1:7860"

If Not fso.FileExists(pythonExe) Then
  MsgBox "Virtual environment not found. Run Setup.bat first.", vbExclamation, "VoiceForge 2762"
  WScript.Quit 1
End If

shell.Run """" & pythonExe & """ """ & fso.BuildPath(baseDir, "run.py") & """", 0, False
WScript.Sleep 3000
shell.Run url

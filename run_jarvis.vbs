' Run Jarvis Assistant without opening terminal window
' This script runs Jarvis in background using virtual environment Python

Option Explicit

Dim oShell
Dim scriptDir
Dim venvPythonPath
Dim jarvisScriptPath
Dim fso

' Create WScript Shell object
Set oShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\") - 1)

' Set paths
venvPythonPath = scriptDir & "\jarvis_env\Scripts\python.exe"
jarvisScriptPath = scriptDir & "\jarvis.py"

' Verify if Python executable exists
If Not fso.FileExists(venvPythonPath) Then
    MsgBox "Erro: O executável do Python não foi encontrado em " & venvPythonPath, vbCritical, "Erro de Configuração"
    WScript.Quit
End If

' Verify if Jarvis script exists
If Not fso.FileExists(jarvisScriptPath) Then
    MsgBox "Erro: O script Jarvis não foi encontrado em " & jarvisScriptPath, vbCritical, "Erro de Configuração"
    WScript.Quit
End If

' Construct the command to run Jarvis
Dim command
command = """" & venvPythonPath & """ """ & jarvisScriptPath & """"

' Run Jarvis hidden
oShell.Run command, 0, False

' Show success message (optional)
MsgBox "Jarvis está iniciando em segundo plano...", vbInformation, "Jarvis"

' Clean up
Set oShell = Nothing
Set fso = Nothing

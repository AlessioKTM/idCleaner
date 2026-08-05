rule Suspicious_Powershell_Download {
    meta:
        description = "Detects obfuscated PowerShell commands or stealth download cradles"
        severity = "HIGH"
    strings:
        $ps1 = "powershell" nocase
        $ps2 = "pwsh" nocase
        $enc = "-enc" nocase
        $e1 = "-encodedcommand" nocase
        $nop = "-nop" nocase
        $hidden = "-w hidden" nocase
        $download1 = "DownloadString" nocase
        $download2 = "DownloadFile" nocase
        $iex = "IEX" nocase
    condition:
        (($ps1 or $ps2) and ($enc or $e1 or $hidden or $nop)) or
        (any of ($download*) and $iex)
}

rule Living_Off_The_Land_Binaries {
    meta:
        description = "Detects usage of legitimate Windows binaries to download payloads (LOLBins)"
        severity = "CRITICAL"
    strings:
        $certutil = "certutil" nocase
        $decode = "-decode" nocase
        $urlcache = "-urlcache" nocase
        $bitsadmin = "bitsadmin" nocase
        $transfer = "/transfer" nocase
        $mshta = "mshta" nocase
        $wscript = "wscript.shell" nocase
    condition:
        ($certutil and ($decode or $urlcache)) or
        ($bitsadmin and $transfer) or
        $mshta or $wscript
}

rule Suspicious_Process_Injection_API {
    meta:
        description = "Detects API imports commonly used for process injection or shellcode execution"
        severity = "CRITICAL"
    strings:
        $mz = { 4D 5A }
        $api1 = "VirtualAllocEx" nocase
        $api2 = "WriteProcessMemory" nocase
        $api3 = "CreateRemoteThread" nocase
        $api4 = "QueueUserAPC" nocase
        $api5 = "NtUnmapViewOfSection" nocase
    condition:
        $mz at 0 and 3 of ($api*)
}

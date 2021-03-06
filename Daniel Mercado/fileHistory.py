## fileHistory.py
## Author: Daniel "Albinohat" Mercado
## This module aims to gather information about recent file history on a Windows machine.

## Standard Imports
import binascii, os, time, win32security

## Third-party Imports
from win32com.shell import shell, shellcon
import easyReg

## RecentFile - This call contains information about a recently opened or saved file.
class RecentFile():
	## __init__   - Initialize the attributes of a registry entry (File).
	## self.entry - The registry entry associated with this file.
	## self.file  - The human-readable name associated with the PIDL stored in self.data.
	## self.meta  - A Metadata object containing metadata about a self.file.
	##
	## entry - The registry object associated with this file.
	def __init__(self, entry):
		self.entry = entry
		## Verify the integrity of the PIDL which should be 20 bytes long.
		if (int(binascii.hexlify(self.entry.data[0:1]), 16) == 20):
			self.file = shell.SHGetPathFromIDList(shell.StringAsPIDL(self.entry.data))
			try:
				self.meta = Metadata(self.file, os.stat(self.file))
		
			except WindowsError:
				self.meta = "File deleted. No metadata available."
		else:
			self.file = "INVALID_FORMAT"

	## printRecentFile - Prints out the attributes of the printRecentFile instance.
	def printRecentFile(self):
		if (self.file != "INVALID_FORMAT"):
			print "    RecentFile.printRecentFile()"
			print "        Value: "   + self.entry.value
			print "        File: "  + self.file
			if (isinstance(self.meta, Metadata)):
				self.meta.printMetadata()
			elif (type(self.meta) is str):
				print "        " + self.meta
		
## End of RecentFile class

## Metadata - This class contains information describing a file.
class Metadata():
	## __init__   - Initialize the attributes of a File
	## self.file  - The name of the file passed in form RegEntry.__init__().
	## self.owner - The owner of the current file. (Tuple)
	## self.sid   - The Security Identifier (SID) of the owner of the current file.
	## self.uid   - A list containing the name, domain and type of the owner of the file.
	## self.size  - The size of the file.
	## self.mtime - The time the file was last modified.
	## self.atime - The time the file was last accessed (opened).
	## self.ctime - The time the file was created.
	##
	## file      - The name of the file passed in from RecentFile.__init__().	
	## f_obj      - The file object passed in from RecentFile.__init__().
	def __init__(self, file, f_obj):
		self.file  = file
		self.sid = win32security.GetFileSecurity(self.file, win32security.OWNER_SECURITY_INFORMATION).GetSecurityDescriptorOwner()
		if (self.file != "INVALID_FORMAT"):
			try:
				self.owner = win32security.LookupAccountSid(None, self.sid)
			except:
				self.owner = "No Matching User for SID: " + str(self.sid)[6:]
		else:
			self.owner = ""
		self.size  = f_obj.st_size
		self.mtime = f_obj.st_mtime
		self.atime = f_obj.st_atime
		self.ctime = f_obj.st_ctime
	
	## printMetadata - Prints out the attributes of the Metadata instance.
	def printMetadata(self):
		print "    Metadata.printMetadata()"
		print     "        SID: " + str(self.sid)[6:]
		if (type(self.owner) is str):
			print "        Owner: "     + str(self.owner)
		else:
			print "        Owner: "     + self.owner[1] + "\\" + self.owner[0]
			
		print "        File Size: " + str(self.size)
		print "        Modified: "  + time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(self.mtime))
		print "        Accessed: "  + time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(self.atime))
		print "        Created: "   + time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(self.ctime)) + "\n"
		
##End of Metadata class

from Products.CMFCore import utils
from Products.Archetypes.public import *
from Products.Archetypes import listTypes
from Products.CMFCore.DirectoryView import registerDirectory
from OFS import Folder

from config import *
import permissions

registerDirectory('skins', GLOBALS)
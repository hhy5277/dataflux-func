'use strict';

/* Builtin Modules */

/* 3rd-party Modules */
var async = require('async');

/* Project Modules */
var E       = require('../utils/serverError');
var CONFIG  = require('../utils/yamlResources').get('CONFIG');
var toolkit = require('../utils/toolkit');

var scriptSetImportHistoryMod = require('../models/scriptSetImportHistoryMod');

/* Configure */

/* Handlers */
var crudHandler = exports.crudHandler = scriptSetImportHistoryMod.createCRUDHandler();

exports.list = crudHandler.createListHandler();

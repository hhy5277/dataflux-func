'use strict';

/* Builtin Modules */

/* 3rd-party Modules */
var async = require('async');

/* Project Modules */
var E       = require('../utils/serverError');
var CONFIG  = require('../utils/yamlResources').get('CONFIG');
var toolkit = require('../utils/toolkit');

var scriptSetMod = require('../models/scriptSetMod');

/* Configure */

/* Handlers */
var crudHandler = exports.crudHandler = scriptSetMod.createCRUDHandler();

exports.list   = crudHandler.createListPage();
exports.add    = crudHandler.createAddPage();
exports.modify = crudHandler.createModifyPage();

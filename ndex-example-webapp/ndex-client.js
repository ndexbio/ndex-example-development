/**
 * Created by dexter on 8/13/17.
 */
// Thanks to http://ourcodeworld.com/
// for the tutorial and code example
// about creating javascript libraries

// This library depends on jquery.js

(function (window) {
    'use strict';

    // This function creates an ndex client object
    function makeNdexClient() {
        var _ndexClientObject = {};

        /*---------------------------------------------------------------------*
         * Client settings
         *---------------------------------------------------------------------*/

        // this is a private variable visible in the scope ndexClient
        var clientSettings = {
            ndexServerUri: "www.ndexbio.org"
        };

        // this is a public function to set a private variable
        _ndexClientObject.setNdexServerUri = function (uri) {
            // TODO - verify that the string is a valid uri
            clientSettings.ndexServerUri = uri;
        };

        // this is a public function to return a private variable value
        _ndexClientObject.getNdexServerUri = function () {
            return clientSettings.ndexServerUri;
        };

        /*---------------------------------------------------------------------*
         * Errors
         *---------------------------------------------------------------------*/
         var ndexError = function (string) {
            console.log(string);
        };

        /*---------------------------------------------------------------------*
         * ID, Authentication, Credentials
         *---------------------------------------------------------------------*/

        // public functions

        _ndexClientObject.clearUserCredentials = function () {
            localStorage.setItem('loggedInUser', null);
        };

        _ndexClientObject.setUserCredentials = function (accountName, externalId, token) {
            if (localStorage) {
                var loggedInUser = {};
                loggedInUser.accountName = accountName;
                loggedInUser.token = token;
                loggedInUser.externalId = externalId;
                localStorage.setItem('loggedInUser', JSON.stringify(loggedInUser));
            }
        };

        _ndexClientObject.getUserCredentials = function () {
            if (localStorage) {
                var loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
                if (loggedInUser === null) {
                    return null;
                }
                return {
                    accountName: loggedInUser.accountName,
                    externalId: loggedInUser.externalId,
                    token: loggedInUser.token
                };
            }
        };

        _ndexClientObject.setUserInfo = function (accountName, externalId) {
            var loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
            if (!loggedInUser) {
                loggedInUser = {};
            }
            loggedInUser.accountName = accountName;
            loggedInUser.externalId = externalId;
            localStorage.setItem('loggedInUser', JSON.stringify(loggedInUser));
        };

        _ndexClientObject.getUserInfo = function () {
            return JSON.parse(localStorage.getItem('loggedInUser'));
        };

        // private functions
/*
        var setUserAuthToken = function (token) {
            var loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
            if (!loggedInUser) {
                loggedInUser = {};
            }
            loggedInUser.token = token;
            localStorage.setItem('loggedInUser', JSON.stringify(loggedInUser));
        };
*/

        /*
         var getLoggedInUserExternalId = function () {
         var loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
         if (!loggedInUser) {
         loggedInUser = {};
         }
         return loggedInUser.externalId;
         };
         */
        var getLoggedInUserAccountName = function () {
            var loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
            if (!loggedInUser) {
                loggedInUser = {};
            }
            return loggedInUser.accountName;
        };

        var getLoggedInUserAuthToken = function () {
            var loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
            if (!loggedInUser) {
                loggedInUser = {};
            }
            return loggedInUser.token;
        };

        /*---------------------------------------------------------------------*
         * Returns the user's credentials as required by Basic Authentication base64
         * encoded.
         *---------------------------------------------------------------------*/

        var getEncodedUser = function () {
            if (getLoggedInUserAccountName() !== undefined && getLoggedInUserAccountName() !== null) {
                return btoa(getLoggedInUserAccountName() + ':' + getLoggedInUserAuthToken());
            } else {
                return null;
            }
        };

        var addAuth = function (encodedUser, options) {
            if (!options.headers){
                options.headers = {}
            }
            if (encodedUser) {
                options.headers.Authorization = 'Basic ' + getEncodedUser();
            }
            else {
                options.headers.Authorization = undefined;
            }
        };

        /*
         var requestWithAbort = function (config) {
         // The $http timeout property takes a deferred value that can abort AJAX request
         var deferredAbort = $q.defer();

         config.timeout = deferredAbort.promise;

         // We keep a reference ot the http-promise. This way we can augment it with an abort method.
         var request = $http(config);

         // The $http service uses a deferred value for the timeout. Resolving the value will abort the AJAX request
         request.abort = function () {
         deferredAbort.resolve();
         };

         // Make garbage collection smoother by forcing the request.abort to an empty function
         // and then set the deferred abort and the request to null
         // This cleanup is performed once the request is finished.
         request.finally(
         function () {
         request.abort = angular.noop; // angular.noop is an empty function
         deferredAbort = request = null;
         }
         );

         return request;
         };
         */

        /*---------------------------------------------------------------------*
         * private function to be an NDEx wrapper around JQuery AJAX
         * returns a jXHR object
         *---------------------------------------------------------------------*/

        // note that only success and error are used in the options parameter
        var ndexAjax = function (method, route, data, options) {
            var url = "http://" + clientSettings.ndexServerUri + "/v2" + route;
            var ajax_options = {};
            if (options) {
                if (options.success) ajax_options.success = options.success;
                if (options.error) ajax_options.error = options.error;
            }
            ajax_options.method = method;
            if (data){
                ajax_options.data = data;
            }
            addAuth(getEncodedUser(), ajax_options);
            return $.ajax(url, ajax_options);
        };

        /*---------------------------------------------------------------------*
         * ****  NDEx REST API  ****
         *  (public functions)
         *---------------------------------------------------------------------*/

        /*---------------------------------------------------------------------*
         * Search
         *---------------------------------------------------------------------*/
        // Search Networks POST /search/network?start={number}&size={number}
        // options:
        // searchString
        // permission
        // includeGroups
        // accountName
        // startPage
        // pageSize
        // success
        // error
        //
        // python: search_networks(self, search_string="", account_name=None, start=0, size=100, include_groups=False)
        _ndexClientObject.searchNetworks = function (options) {
            var pageSize = options.pageSize ? options.pageSize : 100;
            var startPage = options.startPage ? options.startPage : 0;
            var query = {};
            if (options.searchString){
                query.searchString = options.searchString;
            } else {
                ndexError("searchNetworks options must include searchString");
            }
            if (options.includeGroups){
                query.includeGroups = options.includeGroups;
            } else {
                query.includeGroups = false;
            }
            if (options.permission) query.permission = options.permission;
            if (options.accountName) query.accountName = options.accountName;
            return ndexAjax('POST', '/search/network?start=' + startPage + '$size=' + 'pageSize',
                query,
                options);
        };

        // Search Networks by Gene/Protein  POST   /search/network/genes?start={number}&size={number}
        // TODO - does this query use the account / group / permissions parameters?
        _ndexClientObject.searchNetworksGenes = function (options) {
            var pageSize = options.pageSize ? options.pageSize : 100;
            var startPage = options.startPage ? options.startPage : 0;
            var query = {};
            if (options.searchString){
                query.searchString = options.searchString;
            } else {
                ndexError("searchNetworksGenes options must include searchString");
            }
            /*
            if (options.includeGroups){
                query.includeGroups = options.includeGroups;
            } else {
                query.includeGroups = false;
            }
            if (options.permission) query.permission = options.permission;
            if (options.accountName) query.accountName = options.accountName;
            */
            return ndexAjax('POST', '/search/network/genes?start=' + startPage + '$size=' + 'pageSize',
                query,
                options);
        };

        // Search Networks POST /search/user?start={number}&size={number}
        _ndexClientObject.searchUsers = function (options) {
            var pageSize = options.pageSize ? options.pageSize : 100;
            var startPage = options.startPage ? options.startPage : 0;
            var query = {};
            if (options.searchString){
                query.searchString = options.searchString;
            } else {
                ndexError("searchUsers options must include searchString");
            }
            return ndexAjax('POST', '/search/user?start=' + startPage + '$size=' + 'pageSize',
                query,
                options);
        };

        // Search Groups POST /search/group?start={number}&size={number}
        _ndexClientObject.searchGroups = function (options) {
            var pageSize = options.pageSize ? options.pageSize : 100;
            var startPage = options.startPage ? options.startPage : 0;
            var query = {};
            if (options.searchString){
                query.searchString = options.searchString;
            } else {
                ndexError("searchGroups options must include searchString");
            }
            return ndexAjax('POST', '/search/group?start=' + startPage + '$size=' + 'pageSize',
                query,
                options);
        };

        // Get a network 'neighborhood'
        // POST /search/network/{networkId}/query
        // python: get_neighborhood_as_cx_stream(self, network_id, search_string, search_depth=1, edge_limit=2500)
        _ndexClientObject.getNetworkNeighborhood = function (networkId, options) {
            var query = {};
            if (options.searchString){
                query.searchString = options.searchString;
            } else {
                ndexError("getNetworkNeighborhood options must include searchString");
            }
            if (options.searchDepth){
                if (options.searchDepth > 3){
                    ndexError("searchDepth = " + options.searchDepth + " exceeds the maximum of 3");
                }
                query.searchDepth = options.searchDepth;
            } else {
                query.searchDepth = 1;
            }
            if (options.edgeLimit){
                query.edgeLimit = options.edgeLimit;
            } else {
                query.edgeLimit = 1500;
            }
            return ndexAjax('POST', '/search/network' + networkId + '/query', query, options);
        };

        // Advanced Query POST /search/network/{networkId}/advancedquery
        // TODO review function name
        _ndexClientObject.getNetworkFiltered = function (networkId, options) {
            var query = {};
            if (options.nodeFilter){
                query.nodeFilter = options.nodeFilter;
            }
            if (options.edgeFilter){
                query.edgeFilter = options.edgeFilter;
            }
            if (options.edgeLimit){
                query.edgeLimit = options.edgeLimit;
            } else {
                query.edgeLimit = 1500;
            }
            return ndexAjax('POST', '/search/network' + networkId + '/advancedquery', query, options);
        };

        /*---------------------------------------------------------------------*
         * Users
         *---------------------------------------------------------------------*/

        // authenticate user by username and password
        _ndexClientObject.authenticateUser = function (userName, password, options) {
            // Server API: Authenticate User
            // GET /user?valid=true
            var url = "http://" + clientSettings.ndexServerUri + "/v2/user?valid=true";
            var ajax_options = {};
            if (options.success) ajax_options.success = options.success;
            if (options.error) ajax_options.error = options.error;
            ajax_options.headers = {
                'Authorization': "Basic " + btoa(userName + ":" + password)
            };
            return $.ajax(url, ajax_options);
        };

        // TODO get users by uuids


        /*---------------------------------------------------------------------*
         * Groups
         *---------------------------------------------------------------------*/

        // TODO get groups by uuids
        /*---------------------------------------------------------------------*
         * Networks
         *---------------------------------------------------------------------*/

        // Get a Network Summary GET  /network/{networkid}/summary?accesskey={accessKey}
        _ndexClientObject.getNetworkSummary = function (networkId, options) {
            return ndexAjax('GET', '/network/' + networkId + "/summary", null, options);
        };

        // Create a network POST /network
        // Post as form data
        // default processing of data is turned off
        // instead CX is explicitly processed into a blob and appended to
        // the form data using the attribute CXNetworkStream
        //
        // python: save_cx_stream_as_new_network

        _ndexClientObject.createNetwork = function (cx, options) {
            var formData = new FormData();
            var content = JSON.stringify(cx);
            var blob = new Blob([content], { type: "application/octet-stream"});
            formData.append('CXNetworkStream', blob);
            var url = "http://" + clientSettings.ndexServerUri + "/v2/network";
            options.method = "POST";
            options.processData = false;
            options.contentType = false;
            options.data = formData;
            addAuth(getEncodedUser(), options);
            return $.ajax(url, options);
        };

        // this is useful when you want the UUID of a newly created network, not its URL
        _ndexClientObject.getUUIDfromURL = function(networkURL){
            var elements = networkURL.split('/');
            return elements[elements.length - 1];
        };

        // Update a network PUT /network/{networkid}
        _ndexClientObject.updateNetwork = function (networkId, cx, options) {
            var formData = new FormData();
            var content = JSON.stringify(cx);
            var blob = new Blob([content], { type: "application/octet-stream"});
            formData.append('CXNetworkStream', blob);
            var url = "http://" + clientSettings.ndexServerUri + "/v2/network/" + networkId;
            options.method = "PUT";
            options.processData = false;
            options.contentType = false;
            options.data = formData;
            addAuth(getEncodedUser(), options);
            return $.ajax(url, options);
        };

        // Delete a network DELETE /network/{networkid}
        _ndexClientObject.deleteNetwork = function (networkId, ajax_options) {
            return ndexAjax('DELETE', '/network/' + networkId, null, ajax_options);
        };

        // Get Complete Network in CX format GET  /network/{networkid}?accesskey={accessKey}
        // python: get_network_as_cx_stream(self, network_id):
        // (stream vs. complete?)
        _ndexClientObject.getNetwork = function (networkId, ajax_options) {
            return ndexAjax('GET', '/network/' + networkId, null, ajax_options);
        };


        // Get Aspects of a Network POST /batch/network/{networkid}/aspect
        _ndexClientObject.getNetworkAspects = function(networkId, options){
            var query = {};
            if (options.aspects){
                query = options.aspects;
            } else {
                ndexError("getNetworkAspects options must include aspects");
            }
            return ndexAjax('POST', '/batch/network' + networkId + '/aspect', query, options);
        };

        // python: get_network_aspect_as_cx_stream(self, network_id, aspect_name):
        // Get a Network Aspect As CX  GET  /network/{networkid}/aspect/{aspectName}?size={limit}
        _ndexClientObject.getNetworkAspect = function (networkId, options) {
            var aspectName;
            if (options.aspectName) {
                aspectName = options.aspectName;
            } else {
                ndexError("getNetworkAspect options must include aspectName");
            }
            var query = {};
            if (options.size) {
                query.size = options.size;
            }
            return ndexAjax('GET', '/network/' + networkId + '/aspect/' + aspectName, query, options);
        };

        // Update an Aspect of a Network PUT /network/{networkid}/aspect/{aspectName}
        _ndexClientObject.updateNetworkAspect = function (networkId, aspect_name, cx, ajax_options) {
            return ndexAjax('PUT', '/network/' + networkId + '/aspect/' + aspect_name, cx, ajax_options);
        };

        // Get Network Sample GET /network/{networkid}/sample?accesskey={accessKey}
        _ndexClientObject.getNetworkSample = function (networkId, ajax_options) {
            return ndexAjax('GET', '/network/' + networkId + '/sample', null, ajax_options);
        };

        // TODO
        // Set Sample Network PUT
        // /network/{networkid}/sample
        _ndexClientObject.setNetworkSample = function (networkId, cx, ajax_options) {
            return ndexAjax('PUT', '/network/' + networkId + '/sample', cx, ajax_options);
        };

        // Set Network Properties PUT /network/{networkid}/properties
        // Updates the NetworkAttributes aspect the network specified by ‘networkId’
        // based on the list of NdexPropertyValuePair objects in the PUT data.
        _ndexClientObject.setNetworkProperties = function (networkId, property_value_pairs, ajax_options) {
            return ndexAjax('PUT', '/network/' + networkId + '/properties', property_value_pairs, ajax_options);
        };

        _ndexClientObject.setNetworkProfile = function (networkId, properties, ajax_options) {
            return ndexAjax('PUT', '/network/' + networkId + '/profile', properties, ajax_options);
        };

        // Set Network System Properties PUT /network/{networkId}/systemproperty
        _ndexClientObject.setNetworkSystemProperties = function (networkId, properties, ajax_options) {
            return ndexAjax('PUT', '/network/' + networkId + '/systemproperty', properties, ajax_options);
        };

        /*---------------------------------------------------------------------*
         * Network Permissions
         *---------------------------------------------------------------------*/

        // Get All Permissions on a Network GET
        // /network/{networkid}/permission?type={user|group}&permission={permission}&start={startPage}&size={pageSize}
        _ndexClientObject.getNetworkPermissions = function (networkId, type, permission, startPage, pageSize, options) {
            var args = {
                type: type,
                permission: permission,
                start: startPage,
                size: pageSize
            };
            return ndexAjax('GET', '/network/' + networkId + '/permission', args, options);
        };

        // Update Network Permission PUT
        // /network/{networkid}/permission?(userid={uuid}|groupid={uuid})&permission={permission}
        _ndexClientObject.updateNetworkPermission = function (networkId, type, id, permission, options) {
            var args = {permission: permission};
            if (type === 'user'){
                args.userid = id;
            } else if (type === 'group'){
                args.groupid = id;
            }
            return ndexAjax('PUT', '/network/' + networkId + '/permission', args, options);
        };

        // Delete Network Permission DELETE /network/{networkid}/permission?(userid={uuid}|groupid={uuid})
        _ndexClientObject.deleteNetworkPermission = function (networkId, type, id, options) {
            var args = {};
            if (type === 'user'){
                args.userid = id;
            } else if (type === 'group'){
                args.groupid = id;
            }
            return ndexAjax('DELETE', '/network/' + networkId + '/permission', args, options);
        };

        // TODO get network summaries by uuids

        /*---------------------------------------------------------------------*
         * Network Sets
         *---------------------------------------------------------------------*/

/*

 Create a Network Set

 /networkset

 Method: POST

 Authentication: Required

 Description: Create a network set. The posted object should have these 2 fields:

 name: String. A short name for the network set. Names are not unique across all users, but they should be unique within a user.
 description: String. Optional.
 Update a Network Set

 /networkset/{networksetid}

 Method: PUT

 Authentication: Required

 Description:

 Updates a project based on the serialized project object in the PUT data.
 The structure of the posted project should be:
 { “name”: string, “description”: string}
 Delete a Network Set

 /networkset/{networksetid}

 Method: DELETE

 Authentication: Required

 Description: Deletes a network set.

 Get a Network Set

 /networkset/{networksetid}?accesskey={accesskey}

 Method: GET

 Authentication: Not required

 Description:

 Returned object has this structure:
 {
 “name”: string,
 “description” : string,
 “Networks”: [ network_ids]
 }
 Add networks to Network Set

 /networkset/{networksetid}/members

 Method: POST

 Authentication: Required

 Description: Add a list of networks to this set. The posted data is a list of network ids. All the networks should be visible to the owner of network set.

 Delete networks from Network Set

 /networkset/{networksetid}/members

 Method: DELETE

 Authentication: Required

 Description: Delete networks from a networks set. Posted data is a list of network ids.

 Get Access key of Network Set

 /networkset/{networksetid}/accesskey

 Method: GET

 Authentication: Required

 Description: This function returns an access key to the user. This access key will allow any user to have read access to member networks of this network set regardless if that user has READ privilege on that network

 The caller has to be the owner of this network set.
 If an access key was not enabled it reurns http code 204.
 If an access key has been turned on, this function returns the key.
 Disable/Enable Access Key on Network Set

 /networkset/{networksetid}/accesskey?action={disable|enable}

 Method: PUT

 Authentication: Required

 Description: This function turns on/off the access key. It returns the key when it is enabled, and returns http code 204 when it is disabled.

 Update Network Set System Properties

 /networkset/{networksetId}/systemproperty

 Method: PUT

 Authentication: Required

 Description:

 Network Set System properties are the properties that describe the network set’s status in a particular NDEx server.
 Sets the system property specified in the PUT data for the network set specified by networksetid.
 As of NDEx V2.0 the supported system properties are:
 showcase: boolean. Authenticated user can use this property to control whether this network set will display in his or her home page. Caller will receive an error if the user is not the owner of the network set.
 PUT data format: {property: value} such as { “showcase”: true}
 */
        /*---------------------------------------------------------------------*
         * ****  Finally, return the client object  ****
         *---------------------------------------------------------------------*/
        return _ndexClientObject;
    }

    /*---------------------------------------------------------------------*
     * the window variable 'ndex' is set to an instance of _ndexClientObject
     * returned by ndexClient unless 'ndex' is already defined
     * in which case we throw an error
     *---------------------------------------------------------------------*/

    if (typeof(window.ndexClient) === 'undefined') {
        window.ndexClient = makeNdexClient();
    }

})(window); // execute this closure on the global window

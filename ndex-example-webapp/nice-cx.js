/**
 * Created by dexter on 8/17/17.
 */
(function (window) {
    'use strict';

    function makeNiceCXFactory() {
        var _niceCXFactory = {};
        /*---------------------------------------------------------------------*
         * ****  Public NiceCX  Constructors ****
         *---------------------------------------------------------------------*/

        _niceCXFactory.makeNiceCX = function () {
            console.log("Making empty NiceCX object");
            var _niceCXObject = {};


            //_niceCXObject.metadata = MetaDataCollection()
            //_niceCXObject.namespaces = NameSpaces()
            _niceCXObject.nodes = {};
            _niceCXObject.edges = {};
            _niceCXObject.citations = {};
            _niceCXObject.nodeCitations = {};
            _niceCXObject.edgeCitations = {};
            _niceCXObject.supports = {};
            _niceCXObject.nodeAttributes = {};
            _niceCXObject.edgeAttributes = {};
            _niceCXObject.networkAttributes = [];
            _niceCXObject.nodeAssociatedAspects = {};
            _niceCXObject.edgeAssociatedAspects = {};
            _niceCXObject.opaqueAspects = {};
            _niceCXObject.provenance = null;


            _niceCXObject.niceCXError = function (message) {
                console.log("niceCXError = " + message)
            };

            /*---------------------------------------------------------------------*
             * Add elements
             *---------------------------------------------------------------------*/

            _niceCXObject.addNode = function (nodeElement) {
                if (nodeElement['@id'] == undefined) {
                    _niceCXObject.niceCXError('element has no @id property');
                } else {
                    _niceCXObject.nodes[nodeElement['@id']] = nodeElement;
                }
            };

            _niceCXObject.addEdge = function (edgeElement) {
                if (edgeElement['@id'] == undefined) {
                    _niceCXObject.niceCXError('edgeElement has no @id property');
                } else {
                    _niceCXObject.edges[edgeElement['@id']] = edgeElement;
                }
            };

            _niceCXObject.addNetworkAttribute = function (networkAttributeElement) {
                _niceCXObject.networkAttributes.append(networkAttributeElement);
            };


            _niceCXObject.addNodeAttribute = function (nodeAttributesElement) {
                if (nodeAttributesElement['po'] == undefined) {
                    _niceCXObject.niceCXError('nodeAttributesElement has no po property');
                } else {
                    _niceCXObject.nodeAttributes[nodeAttributesElement['po']] = nodeAttributesElement;
                }
            };

            _niceCXObject.addEdgeAttribute = function (edgeAttributesElement) {
                if (edgeAttributesElement['po'] == undefined) {
                    _niceCXObject.niceCXError('edgeAttributesElement has no po property');
                } else {
                    _niceCXObject.edgeAttributes[edgeAttributesElement['po']] = edgeAttributesElement;
                }
            };

            _niceCXObject.addSupport = function (supportElement) {
                if (supportElement['@id'] == undefined) {
                    _niceCXObject.niceCXError('supportElement has no @id property');
                } else {
                    _niceCXObject.supports[supportElement['@id']] = supportElement;
                }
            };

            _niceCXObject.addCitation = function (citationElement) {
                if (citationElement['@id'] == undefined) {
                    _niceCXObject.niceCXError('citationElement has no @id property');
                } else {
                    _niceCXObject.citations[citationElement['@id']] = citationElement;
                }
            };

            _niceCXObject.addNodeCitations = function (node_citation_element) {
                buildManyToManyRelation('nodeCitations', node_citation_element, 'citations');
            };

            _niceCXObject.addEdgeCitations = function (edge_citation_element) {
                buildManyToManyRelation('edgeCitations', edge_citation_element, 'citations');
            };

            var buildManyToManyRelation = function (aspect_name, element, relation_name) {
                var aspect;
                if (aspect_name == 'nodeCitations') {
                    aspect = _niceCXObject.nodeCitations;
                } else if (aspect_name == 'edgeCitations') {
                    aspect = _niceCXObject.edgeCitations
                } else {
                    _niceCXObject.niceCXError('Only nodeCitations and edgeCitations are supported. ' + aspect_name + ' was supplied');
                }
                for (var i = 0; i < element['po'].length; i++) {
                    var aspect_element_id = element['p0'][i];
                    var aspect_element = aspect[aspect_element_id];
                    if (aspect_element == undefined) {
                        aspect[aspect_element_id] = element[relation_name];
                    } else {
                        $.merge(aspect[aspect_element_id], element[relation_name]);
                        $.uniqueSort(aspect[aspect_element_id]);
                    }

                }
            };

            _niceCXObject.addOpaqueAspectElement = function(aspect_name, element) {
                var aspectElements = _niceCXObject.opaqueAspects[aspect_name];
                if (aspectElements == undefined) {
                    aspectElements = [];
                    _niceCXObject.opaqueAspects[aspect_name] = aspectElements;
                }
                aspectElements.append(element);
            };

            _niceCXObject.addNodeAssociatedAspectElement = function(nodeId, aspect_name, element){
                var aspectElements = _niceCXObject.nodeAssociatedAspects[aspect_name];
                if (aspectElements == undefined) {
                    aspectElements = {};
                    _niceCXObject.nodeAssociatedAspects[aspect_name] = aspectElements;
                }
                aspectElements[nodeId] = element;
            };
 /*

            }
                addAssociatatedAspectElement(_niceCXObject.nodeAssociatedAspects, nodeId, elmt)

            var addAssociatatedAspectElement = function(table, id, element){
                aspectElements =

                    table.get(elmt.getAspectName())
                if (aspectElements is None){
                    aspectElements = {}
                    table.put(elmt.
                    getAspectName(), aspectElements)

                    elmts = aspectElements.
                    get(id)

                    if ((elmts is None{

                        elmts = []
                        aspectElements.put(id,

                            elmts)
                        elmts.append(elmt)
*/
            return _niceCXObject;
        };

        _niceCXFactory.makeNiceCXFromCXStream = function (CXStream) {
            var _niceCXObject = _niceCXFactory.makeNiceCX();

            console.log(CXStream);

            return _niceCXObject;

        };
        /*---------------------------------------------------------------------*
         * ****  Finally, return the client object  ****
         *---------------------------------------------------------------------*/
        return _niceCXFactory;
    }

    /*---------------------------------------------------------------------*
     * the window variable 'ndex' is set to an instance of _ndexClientObject
     * returned by ndexClient unless 'ndex' is already defined
     * in which case we throw an error
     *---------------------------------------------------------------------*/

    if (typeof(window.ndexClient) === 'undefined') {
        window.niceCXFactory = makeNiceCXFactory();
    }

})(window); // execute this closure on the global window

/*




 _niceCXObject.addEdgeAssociatedAspectElement = function(edgeId, elmt{
 _niceCXObject.

 addAssciatatedAspectElement(_niceCXObject.edgeAssociatedAspects, edgeId, elmt)

 _niceCXObject.addAssciatatedAspectElement = function(table, id, elmt{
 aspectElements =

 table.get(elmt.getAspectName())
 if (aspectElements is None){
 aspectElements = {}
 table.put(elmt.
 getAspectName(), aspectElements)

 elmts = aspectElements.
 get(id)

 if ((elmts is None{

 elmts = []
 aspectElements.put(id,

 elmts)
 elmts.append(elmt)

 */

/*
 _niceCXObject.getMetadata(self{
 return _niceCXObject.

 metadata

 _niceCXObject.
 setMetadata = function(

 metadata{
 _niceCXObject.metadata = metadata

 _niceCXObject.addNameSpace =

 function(prefix, uri{
 _niceCXObject.namespaces[
 prefix] = uri

 _niceCXObject.

 setNamespaces(self,ns {
 _niceCXObject.namespaces = ns

 _niceCXObject.getNamespaces(self,{
 return _niceCXObject.namespaces

 _niceCXObject.getEdges (self{
 return _niceCXObject.edges

 _niceCXObject.getNodes(self{
 return _niceCXObject.nodes

 _niceCXObject.getOpaqueAspectTable(self{
 return _niceCXObject.opaqueAspects

 _niceCXObject.getNetworkAttributes(self{
 return _niceCXObject.networkAttributes

 _niceCXObject.getNodeAttributes(self{
 return _niceCXObject.nodeAttributes

 _niceCXObject.getEdgeAttributes(self{
 return _niceCXObject.edgeAttributes

 _niceCXObject.getNodeAssociatedAspects(self{
 return _niceCXObject.nodeAssociatedAspects

 _niceCXObject.getEdgeAssociatedAspects(self{
 return _niceCXObject.edgeAssociatedAspects

 _niceCXObject.getNodeAssociatedAspect = function(aspectName{
 return _niceCXObject.nodeAssociatedAspects.get(aspectName)

 _niceCXObject.getEdgeAssociatedAspect = function(aspectName{
 return _niceCXObject.edgeAssociatedAspects.get(aspectName)

 _niceCXObject.getProvenance(self{
 return _niceCXObject.provenance

 _niceCXObject.setProvenance = function(provenance{
 _niceCXObject.provenance = provenance


 };
 */



/*

 // from CX

 for (var i = 0; i < rawCX.length; i++) {
 var fragment = rawCX[i];
 if ((fragment) {
 var aspectName;
 for (aspectName in fragment) {

 var elements = fragment[aspectName];

 if ((aspectName === 'numberVerification') {

 if ((!niceCX.numberVerification) {
 niceCX.numberVerification = fragment;
 }
 continue;

 } else if ((aspectName === 'status') {

 if ((!niceCX.status) {
 niceCX.status = fragment;
 }
 continue;

 } else if ((aspectName === 'metaData') {

 if ((!niceCX.preMetaData) {

 niceCX.preMetaData = fragment;

 } else if ((!niceCX.postMetaData) {

 niceCX.postMetaData = fragment;
 }
 continue;
 }

 for (var j = 0; j < elements.length; j++) {
 var element = elements[j];
 handleCxElement(aspectName, element, niceCX);
 }
 }
 }
 }

 return niceCX;
 };


 var computePreMetadata = function ( niceCX) {
 var preMetaData=[];
 var d = new Date();
 var currentTime = d.getTime();

 _.forEach( niceCX, function (aspectValues, aspectName) {
 var metadataElement = {
 "consistencyGroup" : 1,
 //    "elementCount" : aspectValues.length,
 "lastUpdate" : currentTime,
 "name" : aspectName,
 "properties" : [ ],
 "version" : "1.0"
 };

 if (( aspectName === 'nodes' ||
 aspectName === 'edges' ||
 aspectName === 'citations' ||
 aspectName === 'supports') {
 var objids = Object.keys(aspectValues);
 metadataElement['elementCount'] = objids.length;
 metadataElement["idCounter"] = Number(objids.reduce (function (a,b) {
 return Number(a) > Number(b) ? a: b;
 }));
 }

 preMetaData.push (metadataElement);
 });

 return { "metaData": preMetaData };
 };

 _niceCXObject.niceCXToRawCX = function(niceCX) {

 var rawCX = [];

 if ((niceCX.numberVerification) {
 rawCX.push(niceCX.numberVerification);
 } else {
 rawCX.push ({
 "numberVerification" : [ {
 "longNumber" : 281474976710655
 }]});
 }

 if ((niceCX.preMetaData) {
 rawCX.push(niceCX.preMetaData);
 } else {
 rawCX.push(computePreMetadata(niceCX));
 }

 for (var aspectName in niceCX) {


 if (((aspectName === 'preMetaData') || (aspectName === 'postMetaData') ||
 (aspectName === 'numberVerification') || (aspectName === 'status')) {
 continue;

 }

 var elements= [];

 if (( aspectName === 'nodes' || aspectName === 'edges' ||
 aspectName === 'citations' || aspectName === 'supports' || aspectName === 'functionTerms') {

 _.forEach( niceCX[aspectName], function (element, id) {
 elements.push(element);
 });
 } else if ((aspectName === 'nodeAttributes' || aspectName === 'edgeAttributes') {
 _.forEach(niceCX[aspectName], function(attributes, id) {
 _.forEach ( attributes, function (attribute, attrName) {
 elements.push(attribute);
 });
 });

 } else if (( aspectName === 'edgeCitations' || aspectName === 'nodeCitations' ) {
 _.forEach(niceCX[aspectName], function (citationIds, elementId) {
 var citation = {'po': [Number(elementId)], 'citations': citationIds} ;
 elements.push ( citation);
 });

 } else if (( aspectName === 'edgeSupports' || aspectName === 'nodeSupports') {
 _.forEach(niceCX[aspectName], function (supportIds, elementId) {
 var support = {'po': [Number(elementId)], 'supports': supportIds} ;
 elements.push ( support);
 });
 }  else {
 elements = niceCX[aspectName]['elements'];
 }

 if (( elements.length > 0 ) {
 var fragment = {};
 fragment[aspectName] = elements;
 rawCX.push(fragment);
 }
 }

 if ((niceCX.postMetaData) {
 rawCX.push(niceCX.postMetaData);
 }

 if ((niceCX.status) {
 rawCX.push(niceCX.status);
 } else {
 rawCX.push ( {
 "status" : [ {
 "error" : "",
 "success" : true
 } ]
 } );
 }

 return rawCX;
 };


 var addElementToAspectValueMap = function (aspectValueMap, element) {
 var attributes = aspectValueMap[element.po];

 if ((!attributes) {
 attributes = {};
 aspectValueMap[element.po] = attributes;
 }

 attributes[element.n] = element;
 };


 var addRelationToRelationAspect = function (aspect, element, relationName) {

 for (var l = 0; l < element.po.length; l++) {
 var srcId = element.po[l];
 var relations = aspect[srcId];
 if (( !relations) {
 aspect[srcId] = element[relationName];
 } else {
 aspect[srcId].push.apply(element[relationName]);
 }
 }
 };



 var handleCxElement = function (aspectName, element, niceCX) {

 var aspect = niceCX[aspectName];

 if ((!aspect) {
 aspect = {};

 niceCX[aspectName] = aspect;
 }

 switch (aspectName) {
 case 'nodes':
 case 'edges':
 case 'citations':
 case 'supports':
 aspect[element['@id']] = element;
 break;
 case 'nodeAttributes':
 addElementToAspectValueMap(aspect, element);
 break;
 case 'edgeAttributes':
 addElementToAspectValueMap(aspect, element);
 break;
 case 'edgeCitations':
 case 'nodeCitations':
 addRelationToRelationAspect(aspect,element, 'citations');
 break;
 case 'edgeSupports':
 case 'nodeSupports':
 addRelationToRelationAspect(aspect,element,'supports');
 break;
 case 'functionTerms':
 aspect[element['po']] = element;
 break;
 default:
 // opaque for now

 if ((!aspect.elements) {
 aspect.elements = [];
 }

 aspect.elements.push(element);
 }
 };

 */
/** utility functions for nice cx */
/*
 _niceCXObject.getNodes = function (niceCX) {
 return _.values(niceCX['nodes']);
 };

 _niceCXObject.getNodeAttributes = function (niceCX) {
 return niceCX['nodeAttributes'];
 };

 _niceCXObject.getEdges = function (niceCX) {
 return _.values(niceCX.edges);
 };

 _niceCXObject.getEdgeAttributes = function (niceCX) {
 return niceCX['edgeAttributes'];
 };

 var stringifyFunctionTerm = function (functionTerm) {
 var params = [];
 angular.forEach(functionTerm.args, function (parameter) {
 if ((parameter.f) {
 params.push(stringifyFunctionTerm(parameter));
 } else {
 params.push(parameter);
 }
 });
 return abbreviate(functionTerm.f)+ '(' + params.join(', ') + ')';
 };


 var abbreviate = function (functionName) {
 var pureFunctionName =functionName;
 var arr = functionName.split(':');
 if ((arr.length=2)
 pureFunctionName = arr[1];

 switch (pureFunctionName) {
 case 'abundance':
 return 'a';
 case 'biologicalProcess':
 return 'bp';
 case 'catalyticActivity':
 return 'cat';
 case 'cellSecretion':
 return 'sec';
 case 'cellSurfaceExpression':
 return 'surf';
 case 'chaperoneActivity':
 return 'chap';
 case 'complexAbundance':
 return 'complex';
 case 'compositeAbundance':
 return 'composite';
 case 'degradation':
 return 'deg';
 case 'fusion':
 return 'fus';
 case 'geneAbundance':
 return 'g';
 case 'gtpBoundActivity':
 return 'gtp';
 case 'kinaseActivity':
 return 'kin';
 case 'microRNAAbundance':
 return 'm';
 case 'molecularActivity':
 return 'act';
 case 'pathology':
 return 'path';
 case 'peptidaseActivity':
 return 'pep';
 case 'phosphateActivity':
 return 'phos';
 case 'proteinAbundance':
 return 'p';
 case 'proteinModification':
 return 'pmod';
 case 'reaction':
 return 'rxn';
 case 'ribosylationActivity':
 return 'ribo';
 case 'rnaAbundance':
 return 'r';
 case 'substitution':
 return 'sub';
 case 'translocation':
 return 'tloc';
 case 'transcriptionalActivity':
 return 'tscript';
 case 'transportActivity':
 return 'tport';
 case 'truncation':
 return 'trunc';
 case 'increases':
 return '->';
 case 'decreases':
 return '-|';
 case 'directlyIncreases':
 return '=>';
 case 'directlyDecreases':
 return '=|';
 default:
 return pureFunctionName;
 }
 };



 var createCXFunctionTerm = function (oldJSONNetwork, jsonFunctionTerm ) {
 var functionTerm = { 'f': getBaseTermStr(oldJSONNetwork , jsonFunctionTerm.functionTermId)};
 var parameters = [];
 _.forEach ( jsonFunctionTerm.parameterIds, function (parameterId) {
 var baseTerm = oldJSONNetwork['baseTerms'][parameterId];
 if (( baseTerm ) {
 parameters.push ( getBaseTermStr(oldJSONNetwork , parameterId));
 } else {
 var paraFunctionTerm = oldJSONNetwork['functionTerms'] [parameterId];
 parameters.push (createCXFunctionTerm(oldJSONNetwork,paraFunctionTerm));
 }
 });
 functionTerm['args'] = parameters;

 return functionTerm;
 };


 // to CX
 */





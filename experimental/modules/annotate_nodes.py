import requests
from ndex.networkn import NdexGraph

def annotate_ndexgraph(G_ndex):
    count = 0
    for node in G_ndex.nodes(data=True):
        if len(node) > 1:
            node_name = node[1].get('name')
            prey = node[1].get('Prey')

            if prey is not None:
                uniprot_dict = lookup_uniprot(prey)

                if uniprot_dict is not None:
                    if uniprot_dict.get('comments') is not None and len(uniprot_dict.get('comments')) > 0:
                        G_ndex.set_node_attribute(node[0],'comments', uniprot_dict.get('comments'))
                    if uniprot_dict.get('function') is not None and len(uniprot_dict.get('function')) > 0:
                        G_ndex.set_node_attribute(node[0],'function', uniprot_dict.get('function'))
                    if uniprot_dict.get('subcellular_location') is not None and len(uniprot_dict.get('subcellular_location')) > 0:
                        G_ndex.set_node_attribute(node[0],'subcellular_location', uniprot_dict.get('subcellular_location'))
                    if uniprot_dict.get('similarity') is not None and len(uniprot_dict.get('similarity')) > 0:
                        G_ndex.set_node_attribute(node[0],'similarity', uniprot_dict.get('similarity'))
                    if uniprot_dict.get('synonyms') is not None and len(uniprot_dict.get('synonyms')) > 0:
                        G_ndex.set_node_attribute(node[0],'synonyms', uniprot_dict.get('synonyms'))
                    if uniprot_dict.get('GO') is not None and len(uniprot_dict.get('GO')) > 0:
                        G_ndex.set_node_attribute(node[0],'GO', uniprot_dict.get('GO'))
                    if uniprot_dict.get('GO_title') is not None and len(uniprot_dict.get('GO_title')) > 0:
                        G_ndex.set_node_attribute(node[0],'GO_title', uniprot_dict.get('GO_title'))

                if count % 50 == 0:
                    print node_name + ' ' + str(count)
        count += 1

def lookup_uniprot(prey):
    return_dict = {'recommended_name': '', 'function': [], 'subcellular_location': [],'similarity': [], 'synonyms': [], 'GO': [], 'GO_title': []}
    look_up_json = {}

    #client = pymongo.MongoClient(mongodb_uri)
    #db = client.cache

    #uniprot_full_lookup = db.uniprot_full_lookup

    uniprot_dict_lookup = None #uniprot_full_lookup.find_one({'id': prey})
    if uniprot_dict_lookup is not None:
        look_up_json = uniprot_dict_lookup.get('look_up_resp')
    else:
        url = 'http://www.ebi.ac.uk/proteins/api/proteins/' + prey
        look_up_resp = requests.get(url, headers={'Accept':'application/json'})

        if look_up_resp.ok:
            look_up_json = look_up_resp.json()

    if look_up_json is not None:
        #===================
        # COMMENTS SECTION
        #===================
        comments = look_up_json.get('comments')
        if comments is not None:
            function_array = []
            subcell_array = []
            simularity_array = []
            try:
                for comment in comments:
                    if comment.get('type') == 'FUNCTION':
                        for comment_text in comment.get('text'):
                            function_array.append(comment_text.get('value'))

                    elif comment.get('type') == 'SUBCELLULAR_LOCATION':
                        if comment.get('text') is not None:
                            for comment_text in comment.get('text'):
                                subcell_array.append(comment_text.get('value'))

                    elif comment.get('type') == 'SIMILARITY':
                        for comment_text in comment.get('text'):
                            simularity_array.append(comment_text.get('value'))

                return_dict['function'] = function_array
                return_dict['subcellular_location'] = subcell_array
                return_dict['similarity'] = simularity_array
            except Exception as e:
                print 'Issue with comments'
                print e.message


        #===================
        # PROTEIN SECTION
        #===================
        recommendedName = ''
        try:
            recommendedName = look_up_json.get('protein').get('recommendedName').get('fullName').get('value')
        except Exception as e:
            print 'No protein section'

        return_dict['recommended_name'] = recommendedName

        #===================
        # GENE SECTION
        #===================
        synonyms = []
        try:
            synonyms_array = look_up_json.get('gene')[0].get('synonyms')
            for syn in synonyms_array:
                synonyms.append(syn.get('value'))
        except Exception as e:
            print 'No synonyms section'

        return_dict['synonyms'] = synonyms

        #=======================
        # GO ANNOTATION SECTION
        #=======================
        go_annotations = []
        go_annotations_title = []
        try:
            dbReferences_array = look_up_json.get('dbReferences')
            for ref in dbReferences_array:
                if ref.get('type') == 'GO':
                    term = ref.get('properties').get('term')
                    if term is not None and term.startswith('P:'):
                        go_annotations.append('http://amigo.geneontology.org/amigo/term/' + ref.get('id'))
                        go_annotations_title.append(term[2:] + ' (' + ref.get('id') + ')')
        except Exception as e:
            print 'No synonyms section'

        return_dict['GO'] = go_annotations
        return_dict['GO_title'] = go_annotations_title

        #uniprot_full_lookup.save({'id': prey, 'look_up_resp': look_up_resp})

        return return_dict
    else:
        return None

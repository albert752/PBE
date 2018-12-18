var http = require('http');
var fs = require('fs');
var url = require('url');
var MongoClient = require('mongodb').MongoClient;
var dateFormat = require('dateformat');
var url_db = "mongodb://localhost:27017/";
const querystring = require('querystring');


http.createServer( function (request, response) {
    var query = request.url
    console.log("[SRV] Received " + query + " as query.")
    if (query == "/"){
        console.log("[HTM] Response as webpage")
        show_API_info(response)
    }else if( query == "/favicon.ico"){
	console.log("[HTM] Response as webpage")
        show_API_info(response)
    }else{
        console.log("[API] Response as API")
        request_db(query, response)
    }
    console.log("[SRV] Done with user\n")
}).listen(8081);

console.log('Server running at http://127.0.0.1:8081/\n');

function show_API_info(response){
    fs.readFile("index.html", function (err, data) {
        if (err) {
            console.log(err);
            response.writeHead(404, {'Content-Type': 'text/html'});
        } else {
            response.writeHead(200, {'Content-Type': 'text/html'});
            response.write(data.toString());
        }
        response.end();
    });
}


function request_db(path, response){
    var collection=path.split('/')[1].split('?')[0];
    MongoClient.connect(url_db, { useNewUrlParser: true }, function(err, db) {
        limit_and_query = parse_query(path);
        if (err) throw err;
        var database = db.db("suparurdinado");
		var and_expression = {};
		if(limit_and_query[1].length > 0){
            		and_expression["$and"]= limit_and_query[1];
		}
		console.log(and_expression);
        database.collection(collection).find(and_expression, { _id:0, uid:0}).limit(limit_and_query[0]).sort({date: 1}).toArray( function(err, result) {
            if (err) {
                console.log(err);
                response.writeHead(404, {'Content-Type': 'text/html'});
            } else {
                response.writeHead(200, {'Content-Type': 'text/html'});
                response.write(JSON.stringify(result));
            }
            db.close();
            response.end();
        });
    });
}

function parse_query(path){
	var query=path.split('/')[1].split('?');
	var parsed_query=[];
	var limited=0
	if (query.length  > 1){
		var list_criteria=query[1].split('&');
		for (i=0; i<list_criteria.length; i++){
			if(list_criteria[i].includes("now")){
				var now = new Date();
				list_criteria[i]=list_criteria[i].replace('now', dateFormat(now, "yyyy-mm-dd"));
				console.log();
			}
			if(list_criteria[i].includes("limit")){
			    	limited=parseInt(list_criteria[i].slice(6));
					list_criteria.splice(i,1);
				}
				else if (list_criteria[i].indexOf('[') != -1){

				    //var end_of_comparator_index=list_criteria[i].indexOf(']');
					var comparator_index=[list_criteria[i].indexOf('['), list_criteria[i].indexOf(']')];
					//var criteria = list_criteria[i].slice(0, list_criteria[i].indexOf('['));
				    //var comparator=list_criteria[i].slice(list_criteria[i].indexOf('[')+1, end_of_comparator_index);
					var comparator=[list_criteria[i].slice(0, comparator_index[0]), list_criteria[i].slice(comparator_index[0]+1, comparator_index[1])];
				    //var query_string=list_criteria[i].replace(list_criteria[i].substring(list_criteria[i].indexOf('['), end_of_comparator_index+1),'');
					var query_string=list_criteria[i].replace(list_criteria[i].substring(comparator_index[0], comparator_index[1]+1),'');
					console.log(query_string, comparator);
				    parsed_query.push(querystring.parse(query_string));
				if ('date' in parsed_query[i]){
					parsed_query[i]['date']=new Date(parsed_query[i]['date'])
				}
				if ('hour' in parsed_query[i]){
                                        parsed_query[i]['hour']=parseFloat(parsed_query[i]['hour']);
                                    }

				if ('mark' in parsed_query[i]){
				    	parsed_query[i]['mark']=parseFloat(parsed_query[i]['mark']);
				    }
		        		var dict={}
		        		dict['$'+comparator[1]]=parsed_query[i][comparator[0]];
		        		parsed_query[i][comparator[0]]=dict;
		    }
		    else{
		        parsed_query.push(querystring.parse(list_criteria[i]));
			if ('date' in parsed_query[i]){
                        	parsed_query[i]['date']=new Date(parsed_query[i]['date'])
                        }
			if ('hour' in parsed_query[i]){
                       		parsed_query[i]['hour']=parseFloat(parsed_query[i]['hour']);
                        }
			if ('mark' in parsed_query[i]){
		        	parsed_query[i]['mark']=parseInt(parsed_query[i]['mark']);
		        }

		    }
    	}
	}
	console.log(parsed_query)
    return [limited, parsed_query]
}

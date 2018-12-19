        function on_button() {
            var xhttp = new XMLHttpRequest();
            var query = document.getElementsByName('entry')[0].value
            if (!query.includes('?')) {
                query = query + '?';
            }
            query = query + "&uid=" + document.getElementsByName('uid')[0].value
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    if (this.responseText == "[]") {
                        document.getElementById("alerts").setAttribute("class", "alert alert-danger ");
                        document.getElementById("alerts").style.visibility = "";
                        document.getElementById("alert_text").innerHTML = "<strong>Oh snap!</strong> The UID or the requested information must be wrong."
                        document.getElementById("results").setAttribute("id", "results_hidden");
                    } else {
                        get_name()
                        CreateTableFromJSON(JSON.parse(this.responseText), query.split("?")[0])
                    }
                }
            };
            xhttp.open("POST", query, true);
            xhttp.setRequestHeader("Content-type", "application/json");
            xhttp.send("JSON Data");
        }

        function get_name() {
            var xhttp = new XMLHttpRequest();
            var query = "Users?&uid=" + document.getElementsByName('uid')[0].value;
            var text = "<strong>Everything Ok!</strong> This is the information you requested, ";
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    text = text + JSON.parse(this.responseText)[0]["user_name"];
                    text = text + '.';
                    document.getElementById("alerts").setAttribute("class", "alert alert-success ");
                    document.getElementById("alerts").style.visibility = "";
                    document.getElementById("alert_text").innerHTML = text;
                }
            };
            xhttp.open("POST", query, true);
            xhttp.setRequestHeader("Content-type", "application/json");
            xhttp.send("JSON Data");
        }

        function CreateTableFromJSON(data, title) {
            document.getElementById("greeter").innerHTML = title;
            var col = [];
            for (var i = 0; i < data.length; i++) {
                for (var key in data[i]) {
                    if (col.indexOf(key) === -1) {
                        col.push(key);
                    }
                }
            }

            var table = document.createElement("table");
            table.setAttribute("class", "table");
            var tr = table.insertRow(-1);

            for (var i = 0; i < col.length; i++) {
                var th = document.createElement("th");
                th.innerHTML = col[i];
                tr.appendChild(th);
            }

            for (var i = 0; i < data.length; i++) {

                tr = table.insertRow(-1);

                for (var j = 0; j < col.length; j++) {
                    var tabCell = tr.insertCell(-1);
						if(col[j] == "date"){
							tabCell.innerHTML = data[i][col[j]].split("T")[0]
						}else{ 
                    		tabCell.innerHTML = data[i][col[j]];
                		}
            	}		
			}

            var divContainer = document.getElementById("showData");
            divContainer.innerHTML = "";

            divContainer.appendChild(table);
            document.getElementById("results_hidden").setAttribute("id", "results");
        }

        function on_cross() {
            document.getElementById("alerts").style.visibility = "hidden";
        }
        document.addEventListener('keyup', function(event) {
            if (event.keyCode == 13) {
                on_button()
            } else if (event.keyCode == 39) {
				document.getElementById("egg").setAttribute("id", "on_egg");
                alert('I would love to say thank you\nto my PBE colleagues <3\n\n(c) by IAG+L');
            } else if (event.keyCode == 37) {
                alert('4B82F395');
			}
		});



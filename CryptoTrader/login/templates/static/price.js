var livePrice = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en";
$(document).ready(function() {
    var coinsDiv = document.getElementById("coins");

    $.ajax(livePrice).done(function(response){
        for (var i = 0; i < response.length; i++) {
            var coinData = response[i];
            var coinDiv = document.createElement("div");
            coinDiv.className = "coin-price";
            coinDiv.innerHTML = "<div class='logo'><img src='" + coinData.image + "'></div>" +
                                "<div>" +
                                    "<h3>£<span id='" + "test" + "'></span></h3>" +
                                    "<h3>" + coinData.name + "</h3>" +
                                    "<button id='viewgraph' onClick='drawgraph(\"" + coinData.id + "\")'>View graph</button>" +
                                "</div>";
            coinsDiv.appendChild(coinDiv);
        }
    });
});
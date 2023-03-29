var btc = document.getElementById("bitcoin")
var eth = document.getElementById("ethereum")
var doge = document.getElementById("dogecoin")
var sol = document.getElementById("solana")

var livePrice = {
    'async': true,
    'scroosDomain': true,
    'url': 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum%2Cdogecoin%2Csolana&vs_currencies=gbp',

    'method': "GET",
    'headers': {},
}

$.ajax(livePrice).done(function(response){
    btc.innerHTML = response.bitcoin.gbp
    eth.innerHTML = response.ethereum.gbp
    doge.innerHTML = response.dogecoin.gbp
    sol.innerHTML = response.solana.gbp
})


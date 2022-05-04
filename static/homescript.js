coinelem = document.getElementById('coin');
qtyinput = document.getElementById('qtyinput');

[coinelem,qtyinput].forEach(function(element) {
    element.addEventListener("change", function () {
        qtyelement = document.getElementById("qtyinput").value;
        currentbalanceElem = document.getElementById('currentBalance').innerHTML
        calculateamount = document.getElementById("calculatedAmount")
        calculateamount.innerHTML = parseFloat(coinelem.value.split(",")[1]) * parseFloat(qtyelement);
        enableBuyButton()
    });
})

qtyinput.addEventListener("keyup", function () {

    qtyelement = document.getElementById("qtyinput").value;
    currentbalanceElem = document.getElementById('currentBalance').innerHTML
    calculateamount = document.getElementById("calculatedAmount")
    calculateamount.innerHTML = parseFloat(coinelem.value.split(",")[1]) * parseFloat(qtyelement);
    enableBuyButton()
});
function maxbuy(){
    currentbalanceElem = document.getElementById('currentBalance').innerHTML;
    coinprice = parseFloat(document.getElementById('coin').value.split(",")[1]);
    qtyelement = document.getElementById("qtyinput");
    console.log("Max button working",currentbalanceElem/coinprice);

    qtyelement.value = currentbalanceElem/coinprice;
    document.getElementById("calculatedAmount").innerHTML = coinprice * parseFloat(qtyelement.value);
    enableBuyButton()
};
function enableBuyButton(){
    calculateamount = parseFloat(document.getElementById("calculatedAmount").innerHTML)
    currentbalanceElem = document.getElementById('currentBalance').innerHTML
    console.log(currentbalanceElem)
    if (calculateamount >0 & currentbalanceElem-calculateamount>=0){
        document.getElementById('buybut').disabled = false
        document.getElementById('buybut').className="buybutEnabled"
    } else {
        document.getElementById('buybut').disabled = true  
        document.getElementById('buybut').className="buybutDisabled"
    }
}

function sell(rowId, amount) {
    window.location = "/sell" + '?rowId=' + rowId + "&amount=" + amount
};

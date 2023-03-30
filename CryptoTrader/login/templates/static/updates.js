
function updatePortfolio() {
    $.ajax({
        url: '/account',   
        type: 'get',
        dataType: 'json',
        success: function(data) {
            // call the function to update the page with the new data
            updatePage(data);
        },
        error: function(xhr, status, error) {
            console.log('Error: ' + error.message);
        }
    });
}

function updatePage(data) {
    let updatebalance = data
    console.log(updatebalance)

    chart.data.datasets[0].data = data.balance_history;
    chart.update();
}

$(document).ready(function() {
    // call the function immediately to get the initial data
    updatePortfolio();

    // call the function once per minute to get updated data
    setInterval(updatePortfolio, 60000);
});

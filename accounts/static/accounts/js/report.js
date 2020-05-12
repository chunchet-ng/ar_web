$( "input#id_transaction__transact_date_0" ).wrap(function() {
    return "<label for='id_transaction__transact_date_0' style='margin-right: 10px;'>From</label>";
});
$( "input#id_transaction__transact_date_1" ).wrap(function() {
    return "<label for='id_transaction__transact_date_1' style='margin-left: 10px;'>To</label>";
});
$( "table.table thead" ).prepend(function() {
    return "<tr><th></th><th></th><th colspan='3' style='text-align:center'>Allowable Requisite Equivalent To</th><th></th></tr>";
});
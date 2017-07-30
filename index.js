//helper sort method
var sort_by = function(field, reverse, primer) {

    var key = primer ?
        function(x) { return primer(x[field]) } :
        function(x) { return x[field] };

    reverse = !reverse ? 1 : -1;

    return function(a, b) {
        return a = key(a), b = key(b), reverse * ((a > b) - (b > a));
    }
}

//high to low by views, where objects is an array of json objects
function sortByViews(objects) {
    objects.sort(sort_by('views', true, parseInt))
}

//high to low by impact score, where objects is an array of json objects
function sortByRating(objects) {
    objects.sort(sort_by('score', true, parseFloat))
}
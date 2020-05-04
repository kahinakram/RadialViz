/**
 * Normalize all data between 
 * 0 - maxLength 
 * @keys the day strings
 * For each day normalize for AM and PM 
 * and find the max value (AM or PM)
 * @return array
 * */
function normalizeData(input_data, keys, maxLength){

    keys.forEach(function (day, i){

        var day_obj = input_data[day];
        var maxAm = d3.max(day_obj.AM, function (d) { return d });
        var maxPm = d3.max(day_obj.PM, function (d) { return d });
        var max_ = Math.max(maxAm, maxPm);

        day_obj.AM.forEach(function (value, j){
            day_obj.AM[j] = (value / max_) * maxLength;
        });

        day_obj.PM.forEach(function (value, j){
            day_obj.PM[j] = (value / max_) * maxLength;
        });

        day_obj['max'] = max_;

        input_data[day] = day_obj;

    });

    return input_data;
}
/**
 * Find all indices for value
 * @return array
 * */
function findIndexes(array, value){
    
    var index = [], i = -1;
    while ((i = array.indexOf(value, i + 1)) != -1){
        index.push(i);
    }
    return index;
}
/** 
* Find Max of array
* @return number
**/
function findMaxOfArray(array){
    return d3.max(array, function (d) { return d });
}
/**
* Find Min of array
* @return number
*/
function findMinOfArray(array){
    return d3.min(array, function (d) { return d });
}
/**
 * Find Max of two values 
 * @return number
*/
function findMaxOfTwoNumb(var1, var2){
    return var1 > var2 ? var1 : var2;
}
/**
 * Find Min of two values 
 * @return number
 */
function findMinOfTwoNumb(var1, var2){
    return var1 < var2 ? var1 : var2;
}
/** 
 * Create Answer String
 * Take values from array and parse it to one string
 * @return string
 * **/
function createAnswerString(input_array, hour){
    
    var answer_string = '';
    input_array.forEach(function (index){
        //match experiment environment
        if (index == 0) { index = 12; }
        answer_string += index.toString() + hour;
    });
    return answer_string;
}
/**
 * Subtracks elements in two arrays
 * @return array
 * */
function subTracksTwoArrys(array1, array2){
    
    var res = [];
    res = array1.map(function (item, index){
        return Math.abs(item - array2[index]);
    })
    return res;
}

function addText(json_obj){
    document.getElementById("textArea").value = '';
    var pretty = JSON.stringify(json_obj, undefined, 4);
    document.getElementById("textArea").value += pretty;
}


/**
 * 
 * @param {*} json_file to serverside 
 */
function uploadJsonToServer(json_file) {
    // POST the Json object to Backend 
    fetch('/createcsv', {
        // Specify the method
        method: 'POST',
        // A JSON payload
        body: JSON.stringify(json_file)
    })
    .then(function (response){
        // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (text){
        // Should be 'OK' if everything was successful
        console.log('Response from server: ', text);
    });
}
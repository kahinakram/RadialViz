/**
 * 
 * @param {*} rawDataObj 
 * @return json object of correct answers for the shown img
 */
function createAnswersJson(rawDataObj,img_nr) {

    // Find min&max for AM
    var maxAm = findMaxOfArray(rawDataObj.AM);
    var minAm = findMinOfArray(rawDataObj.AM);
    const find_max_am = findIndexes(rawDataObj.AM, maxAm);
    const find_min_am = findIndexes(rawDataObj.AM, minAm);

    //Parse the index number to string for easier comparison
    //in the experiment environment.     
    var max_am_string = createAnswerString(find_max_am, 'am');
    var min_am_string = createAnswerString(find_min_am, 'am');

    // Find min&max for PM
    var maxPm = findMaxOfArray(rawDataObj.PM);
    var minPm = findMinOfArray(rawDataObj.PM);
    const find_max_pm = findIndexes(rawDataObj.PM, maxPm);
    const find_min_pm = findIndexes(rawDataObj.PM, minPm);
    
    //Parse the index number to string for easier comparison
    //in the experiment environment. 
    var max_pm_string = createAnswerString(find_max_pm, 'pm');
    var min_pm_string = createAnswerString(find_min_pm, 'pm');

    /////////////////////////////////////////////////////
    //Find Min Across AM/PM
    var lowest_across = '';

    if (rawDataObj.AM[find_min_am[0]] < rawDataObj.PM[find_min_pm[0]]){
        //console.log('MIN AM',find_min_am);
        lowest_across = createAnswerString(find_min_am, 'am');
    } else if (rawDataObj.AM[find_min_am[0]] > rawDataObj.PM[find_min_pm[0]]){
        //console.log('MIN PM',find_min_pm);
        lowest_across = createAnswerString(find_min_pm, 'pm');
    } else{
        lowest_across = createAnswerString(find_min_am, 'am') +
            createAnswerString(find_min_pm, 'pm')
    }
    //Find Max Across AM/PM
    var highest_across = '';

    if (rawDataObj.AM[find_max_am[0]] > rawDataObj.PM[find_max_pm[0]]){
        highest_across = createAnswerString(find_max_am, 'am');
    } else if (rawDataObj.AM[find_max_am[0]] < rawDataObj.PM[find_max_pm[0]]){
        highest_across = createAnswerString(find_max_pm, 'pm');
    } else{
        highest_across = createAnswerString(find_max_am, 'am') +
            createAnswerString(find_max_pm, 'pm')
    }

    /////////////////////////////////////////////////////
    var differenceArray = subTracksTwoArrys(rawDataObj.AM, rawDataObj.PM)

    //Most similar 
    var differenceArray_min = findMinOfArray(differenceArray);
    var findAllMinPos = findIndexes(differenceArray, differenceArray_min);

    //Most Difference 
    var differenceArray_max = findMaxOfArray(differenceArray);
    var findAllMaxPos = findIndexes(differenceArray, differenceArray_max);

    //You have to parse them to strings
    var most_similar = createAnswerString(findAllMinPos,'-');
    var most_different = createAnswerString(findAllMaxPos,'-');

    /////////////////////////////////////////////////////
    //Range answers 

    var range_options_of_three = {
        '1': [1, 2, 3],
        '2': [2, 3, 4],
        '3': [3, 4, 5],
        '4': [4, 5, 6],
        '5': [5, 6, 7],
        '6': [6, 7, 8],
        '7': [7, 8, 9],
        '8': [8, 9, 10],
        '9': [9, 10, 11],
        '10': [10, 11, 0]
    };
    var range_options_of_twelve = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0];

    var short_range = '', long_range = '';

    for (const key of Object.keys(range_options_of_three)){
        
        var am_short_range_sum = 0;
        var pm_short_range_sum = 0;
        var am_long_range_sum = 0;
        var pm_long_range_sum = 0;

        range_options_of_three[key].forEach(function (d){
            
            am_short_range_sum += rawDataObj.AM[d];
            pm_short_range_sum += rawDataObj.PM[d];
            
        });
        am_short_range_sum = key+'am'+am_short_range_sum + '-'; 
        pm_short_range_sum = key + 'pm' + pm_short_range_sum + '-';  
        
        short_range += (am_short_range_sum+pm_short_range_sum);
        
    }
    //Loop
    range_options_of_twelve.forEach(function (d){
        
        am_long_range_sum += rawDataObj.AM[d];
        pm_long_range_sum += rawDataObj.PM[d];
    })
    
    
    am_long_range_sum = 'am' + am_long_range_sum + '-';
    pm_long_range_sum = 'pm' + pm_long_range_sum + '-';
    
    long_range += (am_long_range_sum + pm_long_range_sum);
    
    return {
        'fileName': img_nr,
        'answers': {            
            // Max/Min answers
            'At what time for AM is the value the lowest?': [min_am_string],
            'At what time for AM is the value the highest?': [max_am_string],
            'At what time for PM is the value the lowest?': [min_pm_string],
            'At what time for PM is the value the highest?': [max_pm_string],
            // Max/Min across both AM/PM answers 
            'Across both AM and PM, at what time is the value the lowest?': [lowest_across],
            'Across both AM and PM, at what time is the value the highest?': [highest_across],
            // Similarity answers 
            'At what time is the value for AM and PM most similar?': [most_similar],
            'At what time is the value for AM and PM most different?': [most_different],
            //Range answers
            'Which range of 3 for AM and PM': [short_range],
            'Which range of 12 for AM and PM': [long_range],
        }
    };
}
/**
 * 
 * @param {*} divId 
 * @param {*} img_nr 
 * @return SVG file of divId with img_nr as name
 */
function printSVG(divId, img_nr) {
    var svg_data = document.getElementById(divId).innerHTML //put id of your svg element here

    var head = '<svg title="graph" version="1.1" xmlns="http://www.w3.org/2000/svg">'

    //if you have some additional styling like graph edges put them inside <style> tag

    var style = '<style>circle {cursor: pointer;stroke-width: 1.5px;}' + '\
                text {font: 16px arial;}path {stroke: DimGrey;stroke-width: 1.5px;}</style>'

    var full_svg = head + svg_data + style + "</svg>"
    var blob = new Blob([full_svg], { type: "image/svg+xml" });
    
    saveAs(blob, img_nr + ".svg");
}
function printPNG(divId, img_nr){
    saveSvgAsPng(document.getElementsByTagName('svg')[0], img_nr+".png", { scale: 2, backgroundColor: "#FFFFFF" });
}
var comp = app.project.activeItem;  // Get the current composition
if (comp && comp instanceof CompItem) {
    var file = File.openDialog("Select SRT File", "*.srt");
    if (file) {
        file.open("r");
        var srtText = file.read();
        file.close();

        var regex = /(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?)(?=\n{2,}|\n*$)/g;
        var matches = [];
        var match;
        while ((match = regex.exec(srtText)) !== null) {
            matches.push(match);
        }

        var searchStringsInput = prompt("请输入要检测的字符串列表，用逗号分隔\n例如: 殺し,殺す", "殺し,殺す");
        var searchStrings = splitAndClean(searchStringsInput);

        var topLayer = comp.layers[1];
        for (var i = 0; i < matches.length; i++) {
            var text = matches[i][4];  
            var startTime = matches[i][2];
            var endTime = matches[i][3];
            
            var startSeconds = timeToSeconds(startTime);
            var endSeconds = timeToSeconds(endTime);

            var newLayer = topLayer.duplicate();
            newLayer.name = "SRT Text " + (i + 1);

            newLayer.startTime = startSeconds;
            newLayer.outPoint = endSeconds;

            var textProp = newLayer.property("Source Text");
            var textDocument = textProp.value;
            textDocument.text = text;
            textProp.setValue(textDocument);
            
            applyTextHighlighting(newLayer, text, searchStrings);
        }
        alert("SRT file processed successfully!");
    }
} else {
    alert("Please select a composition.");
}

function timeToSeconds(timeStr) {
    var parts = timeStr.split(':');
    var hours = parseInt(parts[0], 10);
    var minutes = parseInt(parts[1], 10);
    var seconds = parseFloat(parts[2].replace(',', '.'));
    return hours * 3600 + minutes * 60 + seconds;
}

function splitAndClean(input) {
    var result = [];
    var current = "";
    for (var i = 0; i < input.length; i++) {
        if (input[i] === ",") {
            if (current !== "") {
                result.push(current);
                current = "";
            }
        } else {
            current += input[i];
        }
    }
    if (current !== "") {
        result.push(current);
    }
    for (var j = 0; j < result.length; j++) {
        var str = result[j];
        while (str.charAt(0) === " ") {
            str = str.substring(1);
        }
        while (str.charAt(str.length - 1) === " ") {
            str = str.substring(0, str.length - 1);
        }
        result[j] = str;
    }
    return result;
}

function applyTextHighlighting(layer, text, searchStrings) {
    if (!layer.property("Source Text")) {
        alert("Error: Layer is not a text layer.");
        return;
    }
    
    var animators = layer.property("文本动画");
    if (!animators) {
        alert("Error: Cannot access Text Animators on the layer.");
        return;
    }
    
    var animator = animators.addProperty("ADBE Text Animator");
    if (!animator) {
        alert("Error: Failed to create Text Animator.");
        return;
    }
    animator.name = "Highlight";
    
    var textProps = animator.property("ADBE Text Animator Properties");
    if (!textProps) {
        alert("Error: Failed to access Text Animator Properties.");
        return;
    }
    
    var fillColor = textProps.addProperty("ADBE Text Fill Color");
    if (!fillColor) {
        alert("Error: Failed to create Fill Color property.");
        return;
    }
    fillColor.setValue([1, 0.27, 0]); // 橙红色

    var rangeSelector = animator.property("ADBE Text Selectors").addProperty("ADBE Text Range Selector");
    if (!rangeSelector) {
        alert("Error: Failed to create Range Selector.");
        return;
    }
    
    for (var j = 0; j < searchStrings.length; j++) {
        var keyword = searchStrings[j];
        var startIndex = text.indexOf(keyword);
        if (startIndex !== -1) {
            var percentageStart = (startIndex / text.length) * 100;
            var percentageEnd = ((startIndex + keyword.length) / text.length) * 100;
            rangeSelector.property("ADBE Text Selector Start").setValue(percentageStart);
            rangeSelector.property("ADBE Text Selector End").setValue(percentageEnd);
        }
    }
}

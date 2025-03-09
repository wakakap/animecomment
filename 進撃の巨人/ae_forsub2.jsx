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
            
            var startSeconds = timeToSeconds(startTime)-3; // 3秒前
            var endSeconds = timeToSeconds(endTime)+3;

            var newLayer = topLayer.duplicate();
            newLayer.name = "SRT Text " + (i + 1);

            newLayer.startTime = startSeconds;
            newLayer.outPoint = endSeconds;

            var textProp = newLayer.property("Source Text");
            var textDocument = textProp.value;
            textDocument.text = text;
            textProp.setValue(textDocument);
            
            applyTextHighlighting(newLayer, text, searchStrings);
            addBackgroundShape(newLayer, comp); // 添加背景矩形
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
    if (!(layer instanceof TextLayer)) {
        alert("Error: Layer is not a text layer.");
        return;
    }
    
    var textGroup = layer.property("ADBE Text Properties");
    if (!textGroup) {
        alert("Error: Cannot access text properties group.");
        return;
    }
    
    var animators = textGroup.property("ADBE Text Animators");
    if (!animators) {
        alert("Error: Cannot access Text Animators.");
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
    
    // 标记是否至少有一个关键词匹配
    var hasMatch = false;
    
    // 为每个关键词创建单独的范围选择器
    for (var j = 0; j < searchStrings.length; j++) {
        var keyword = searchStrings[j];
        var startIndex = text.indexOf(keyword);
        if (startIndex !== -1) {
            hasMatch = true;
            var rangeSelector = animator.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
            if (!rangeSelector) {
                alert("Error: Failed to create Range Selector for keyword: " + keyword);
                continue;
            }
            
            var percentageStart = (startIndex / text.length) * 100;
            var percentageEnd = ((startIndex + keyword.length) / text.length) * 100;
            
            var startProp = rangeSelector.property("ADBE Text Percent Start");
            var endProp = rangeSelector.property("ADBE Text Percent End");
            
            if (startProp && endProp) {
                startProp.setValue(percentageStart);
                endProp.setValue(percentageEnd);
            } else {
                alert("Error: Could not find Percent Start or End properties for keyword: " + keyword);
            }
        }
    }
    
    // 如果没有匹配到任何关键词，禁用动画器
    if (!hasMatch) {
        animator.enabled = false; // 禁用动画器，而不是移除
        // alert("No matching keywords found. Highlighting disabled.");
    }
}

function addBackgroundShape(textLayer, comp) {
    // 创建形状层
    var shapeLayer = comp.layers.addShape();
    shapeLayer.name = textLayer.name + "_BG";
    
    // 设置时间与文本层相同
    shapeLayer.startTime = textLayer.startTime;
    shapeLayer.outPoint = textLayer.outPoint;
    
    // 添加矩形
    var shapeGroup = shapeLayer.property("ADBE Root Vectors Group");
    var rect = shapeGroup.addProperty("ADBE Vector Shape - Rect");  // 这里定义了 rect
    
    // 获取文本层大小
    var textSourceRect = textLayer.sourceRectAtTime(0, false);
    var padding = 20; // 背景比文字多出的像素
    
    // 设置矩形大小
    rect.property("ADBE Vector Rect Size").setValue([
        textSourceRect.width + padding * 2,
        textSourceRect.height + padding * 2
    ]);
    
    // 设置位置，使背景左对齐于文字并向下偏移
    shapeLayer.property("Position").setValue([
        textLayer.property("Position").value[0] + textSourceRect.width/2 + textSourceRect.left,  // 左对齐
        textLayer.property("Position").value[1] -18
    ]);
    
    // 添加填充
    var fill = shapeGroup.addProperty("ADBE Vector Graphic - Fill");
    fill.property("ADBE Vector Fill Color").setValue([0, 0, 0]); // 黑色
    fill.property("ADBE Vector Fill Opacity").setValue(50); // 50%不透明度
    
    // 将形状层移到文本层下方
    shapeLayer.moveAfter(textLayer);
}
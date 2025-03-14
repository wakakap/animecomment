var comp = app.project.activeItem;
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
    
    var hasMatch = false;
    
    // 为每个关键词创建独立的动画器
    for (var j = 0; j < searchStrings.length; j++) {
        var keyword = searchStrings[j];
        var searchText = text;
        var offset = 0;
        
        // 查找所有出现的关键词
        while (searchText.indexOf(keyword) !== -1) {
            var startIndex = searchText.indexOf(keyword) + offset;
            if (startIndex !== -1) {
                hasMatch = true;
                var animator = animators.addProperty("ADBE Text Animator");
                animator.name = "Highlight_" + j + "_" + startIndex;
                
                var textProps = animator.property("ADBE Text Animator Properties");
                var fillColor = textProps.addProperty("ADBE Text Fill Color");
                fillColor.setValue([1, 0.27, 0]); // 橙红色
                
                var rangeSelector = animator.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
                var percentageStart = (startIndex / text.length) * 100;
                var percentageEnd = ((startIndex + keyword.length) / text.length) * 100;
                
                rangeSelector.property("ADBE Text Percent Start").setValue(percentageStart);
                rangeSelector.property("ADBE Text Percent End").setValue(percentageEnd);
                
                // 更新搜索文本和偏移量，继续查找下一次出现
                searchText = searchText.substring(startIndex + keyword.length);
                offset = startIndex + keyword.length;
            }
        }
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
    var rect = shapeGroup.addProperty("ADBE Vector Shape - Rect");
    
    // 获取文本层大小
    var textSourceRect = textLayer.sourceRectAtTime(0, false);
    var padding = 20; // 背景比文字多出的像素
    
    // 设置矩形大小和位置
    rect.property("ADBE Vector Rect Size").setValue([
        textSourceRect.width + padding * 2,
        textSourceRect.height + padding * 2
    ]);
    
    // 设置位置，使背景居中于文字
    shapeLayer.property("Position").setValue([
        textLayer.property("Position").value[0],
        textLayer.property("Position").value[1]-23
    ]);
    
    // 添加填充
    var fill = shapeGroup.addProperty("ADBE Vector Graphic - Fill");
    fill.property("ADBE Vector Fill Color").setValue([0, 0, 0]); // 黑色
    fill.property("ADBE Vector Fill Opacity").setValue(50); // 50%不透明度
    
    // 将形状层移到文本层下方
    shapeLayer.moveAfter(textLayer);
}
import re

def convert_markdown_images_to_details(markdown_text):
    """
    将 Markdown 文本中的图片转换为 <details> 折叠模式。

    Args:
        markdown_text: 原始的 Markdown 文本。

    Returns:
        转换后的 Markdown 文本。
    """

    # 使用正则表达式匹配 <blockquote> 块及其中的 <img> 标签
    pattern = r"(?s)(^>.*?(?:\n>.*?)?)(?=\n\n|\Z)"  # 匹配以 > 开头的段落块, 允许>后跟一个或多个<img...>

    def replace_with_details(match):
        block_content = match.group(1)
        
        img_pattern = r'<img src="([^"]+)" alt="([^"]*)"(?: width="(\d+%?)")?[^>]*>'
        
        images = re.findall(img_pattern, block_content)
        if not images:
            return block_content  # 如果没有找到图片，则保持原样

        # 提取第一个图片的 alt 属性作为 summary
        first_alt = images[0][1] if images else "查看图片"

        # 构建 <details> 块
        details_block = f"<details>\n<summary>{first_alt}</summary>\n"
        # 移除原先的>
        new_block_content = block_content.replace(">", "")
        details_block += new_block_content

        details_block += "\n</details>\n"
        
        return details_block

    # 执行替换
    converted_text = re.sub(pattern, replace_with_details, markdown_text, flags=re.MULTILINE)

    return converted_text


# 示例用法
markdown_input = """
# 进击的巨人情节问题整理

**前言**：进击的巨人是一部跨度10年以上的漫画/动画，我在完全没有剧透的情况下，2013年在爱奇艺上开始看第一季动画，2023年看完动画结局，整个过程经历了恐怖、疑惑、震撼等等许多高强度的情感体验。当抛去这些情绪，问这究竟是一个什么故事时，可以这么回答：
- 地下室前是一个架空悬疑故事，主要问题是巨人从何而来；
- 地下室到艾伦和吉克接触是战争历史剧，主要问题是纷争如何解决。

忽略一些伏笔细节，我们不难看懂这两个部分的剧情内容，但对于艾伦和吉克接触后的剧情，尤其是结尾部分，对于巨人能力、尤米尔能力等「设定」的理解成为了看懂剧情的关键。

**编写原则**：本文档的目的是为了看懂上述内容，对动画和漫画的重要情节进行梳理，努力看懂这部作品，特别是结尾发生了什么，为什么发生。在编写中，~~尽量不展开推理~~，适当推理，立足于原作，防止脑补过多。完整的解释理论的提出放在其他文档编写。

**标记说明**：除了特别篇和完结篇单独说明，其他动画集数采用「总集数」的标记方法，例如 ep.87 表示最终季最后一集「人类的黎明」。对照可参考 [進擊的巨人集數列表](https://zh.wikipedia.org/wiki/%E9%80%B2%E6%93%8A%E7%9A%84%E5%B7%A8%E4%BA%BA%E9%9B%86%E6%95%B8%E5%88%97%E8%A1%A8)。对于漫画来说，因为我看电子版的单行本，所以页数为每卷的第几页，并且因为几乎每一面都没有页码，所以我直接用电子版漫画的显示页数作为标记数字，例如第一卷中显示「13」的那一页在电子版中是第「15」页。每一话的标题可参考 [進擊的巨人漫畫章節列表](https://zh.wikipedia.org/wiki/%E9%80%B2%E6%93%8A%E7%9A%84%E5%B7%A8%E4%BA%BA%E6%BC%AB%E7%95%AB%E7%AB%A0%E7%AF%80%E5%88%97%E8%A1%A8)。下方标题的「第*话」使用漫画的话数和标题。

## 第1话 - 给两千年后的你 二千年後の君へ

manga-1-13：标记页码的一页「13」，这之后只有三笠的番外篇有类似的页码标记。
> <img src="manga-1-15.png" alt="13" width="40%">

manga-1-15-845：看似是介绍年份：「845年」
> <img src="manga-1-17-845.png" alt="845" width="40%">

manga-1-14：树上有一个十字架刻痕
> <img src="manga-1-16-刻痕.png" alt="刻痕" width="40%">

## 第2话 - 那一天 その日

三笠说：「又是 这样吗……」，结合循环说，字面上有两种解读可能，「又是头疼吗」 or 「又是这样的结局」吗
> <img src="manga-1-83-头疼.png" alt="头疼" width="40%">

anime-ep02-1758：漫画没有描写艾伦3人小时候往城内躲避的场景，也没有新兵训练的场景。动画在这部分做了很多补充。其中一个场景中，甚至有疑似艾伦的身影。这个穿着和艾伦和吉克进入格里沙记忆的穿着一致。
> <img src="anime-ep02-1758-艾伦的身影.png" alt="艾伦的身影" width="40%">

## 第7话 - 小刀 小さな刃

manga-2-102：三笠说：
- 「又是这样吗……又失去了家人，又想起了这**疼痛**，又……**从这里开始**。」

这里又是模棱两可的表达：如果是指「之前失去了妈妈卡露拉，现在又失去了艾伦」，「疼痛」和「从这里开始」显得很违和。

结合三笠的外传，时间上三笠的外传结尾正好接着这里。所以也许「疼痛」指的是「失去艾伦的痛」，「从这里开始」指的是之前「从这里逃离」到梦中世界，暂时避免了失去艾伦，可是梦中世界结尾又不可避免失去艾伦，所有不如「回到这里再从这里开始」。这样理解，和梦中世界的魔术师的对话非常吻合。但如果接受这种解释，「从这里逃离」变成了一种主动选择，主动做一个艾伦还活着的梦？还是实质上的一种循环能力或跨可能（平行）世界能力？

> <img src="manga-2-102-三笠躺.png" alt="三笠躺" width="40%">

manga-3-167 | anime-ep12-0449：「家人」前的停顿，和后面那次如出一辙。
> <img src="manga-3-167-家人.png" alt="家人" width="40%">
> <img src="anime-ep12-0449-家人.png" alt="家人" width="40%">

## 外传 - Lost Girls chapter 2. Lost in the Cruel World

动画标题为 第???话 - Lost Girls Lost in the Cruel World。从开头结尾的连接，暂且理解为三笠得知艾伦被吃后，有些自暴自弃，滑行到没气，摔倒后的脑中幻想。

><img src="anime-ova-Lost Girls Lost in the Cruel World-0426-未知.png" alt="？？？" width="40%">

anime-ova-Lost Girls Lost in the Cruel World-0118：这个镜头一个蝴蝶分裂成多个蝴蝶，不免想到三笠的世界分裂成多个可能世界的意味，「庄周梦蝶」/「蝴蝶效应」。（漫画没有）
><img src="anime-ova-Lost Girls Lost in the Cruel World-0118-蝴蝶分裂.png" alt="蝴蝶分裂" width="40%">

anime-ova-Lost Girls Lost in the Cruel World-0303：这里蝴蝶站在一个石榴状的东西上用三笠的声音对三笠说话，台词颇有深意。（漫画没有）
><img src="anime-ova-Lost Girls Lost in the Cruel World-0303-蝴蝶对话.png" alt="蝴蝶对话" width="40%">

- 蝴蝶三笠：**如果你不接受这个现实的话，就重新来过吧，从你想要的地方重新开始**，在那个世界，一切都能如你所愿，但是，即使如此，你依旧无法阻止艾伦的死亡，因为艾伦………

漫画版和动画版有很大出入，漫画中有更多细节，例如漫画中有蝴蝶的箱子，想不起艾伦的脸等情节。并且漫画中并没有要和艾伦一起，而是嘱托艾伦不要死。这里待补充。

anime-ova-Lost Girls Lost in the Cruel World-0606：二人看到本来杀掉父母的土匪被狗咬死了，恶狗面向二人，三笠头痛，狗走开了。
> <img src="anime-ova-Lost Girls Lost in the Cruel World-0606-狗不咬.png" alt="狗不咬" width="40%"> <img src="anime-ova-Lost Girls Lost in the Cruel World-0606-头疼狗不咬.png" alt="头疼狗不咬" width="40%">

manga-LOSTGIRLS-2-35: 漫画中并没有头痛的描写，而强调狗眼睛中三笠的倒影。
> <img src="manga-LOSTGIRLS-2-35-狗.png" alt="头疼狗不咬" width="40%">

anime-ova-Lost Girls Lost in the Cruel World-0726：「不再走进森林」这台词铺垫的也很有深意，这个爹妈没被杀的世界看似很美好。
><img src="anime-ova-Lost Girls Lost in the Cruel World-0726-不再走进森林.png" alt="不再走进森林" width="40%">

anime-ova-Lost Girls Lost in the Cruel World-1044：同样去看调查兵团，但这个世界穿的漂亮。
><img src="anime-ova-Lost Girls Lost in the Cruel World-1044-三笠帽子.png" alt="三笠帽子" width="40%"> <img src="anime-ep01-0917-三笠背柴.png" alt="三笠背柴" width="40%">

后来，太想见艾伦，妈妈得病所以搬到艾伦家附近，三笠觉得是自己造成的，很内疚。（呼应了「一切都如你所愿」）见到艾伦，得知调查兵团解散，城门被封，艾伦决定和阿尔敏坐热气球出去，三笠也要去，艾伦为其围上围巾，约定3天后出发。快到时间时，三笠被镜男拦下：

镜男的造型在动画版遮住了头发部分，从漫画上色来看，镜男的头像是毛线团，或是绕起来的女人的头发，颜色和三笠的黑色头发相反，非黑色。

><img src="manga-LOSTGIRLS-2-138-镜男.png" alt="镜男" width="40%">
><img src="anime-ova-Lost Girls Lost in the Cruel World-1716-镜男.png" alt="镜男" width="40%">

- 镜男的「奇怪」台词：我乃旷世奇才，是知名催眠师，名叫镜男，接下来，我将为各位表演精彩的催眠术。我会将这位天真无邪的少女彻底变成一个无情的杀人犯。……请仔细看我的脸（镜子中映出三笠）……我不能轻易就让你离开这里呢，为了这场表演，我必须用催眠术让你亲手杀人才行呢。所以不如这样吧，我提议，你在这里动手杀了我吧，虽然可以按照刚说的用催眠术让你下手，不过得花点时间。（**此处漫画独有台词**：这也是没办法的，世界是不讲理的，人类也不想被巨人吃……巨人就什么也不说地吃人，不讲理极了对吧，所以……）
  
  ><img src="manga-LOSTGIRLS-2-133-不讲道理129.png" alt="不讲道理129" width="40%">
  
  注意看这里也出现了标记「129」

- （此处漫画独有台词：……小姐我告诉你一个秘密，我已经忍不下去了，在这一晚上工作，向观众表演催眠术，结束了又要到另一个聚会表演）
  ><img src="manga-LOSTGIRLS-2-134-秘密.png" alt="秘密" width="40%">

- （此处漫画独有台词：……**一遍又一遍地，无数遍地重复，这就是我的人生**。怎么样？实在是无聊，没有意义地人生吧。但是……这也是没办法的，我没有选择。但是，**我已经发自内心地忍不下去了**……所以今夜，我要表演绝无仅有的催眠术，用催眠术把纯洁无邪的少女操控，在大家面前让她把我杀了）
  - 这段台词可能是 `镜男 = 尤米尔` 的最强证据。

  ><img src="manga-LOSTGIRLS-2-135-无数遍.png" alt="无数遍" width="40%">

- （此处漫画独有台词：**这就是我最后的催眠术，对这个世界的复仇**……想好了吗？**再不决定时间要没了哦**）

  ><img src="manga-LOSTGIRLS-2-136-复仇.png" alt="复仇" width="40%">

- （此处漫画独有台词：你不会再见到**艾伦**了 三笠：你是谁？你为什么会知道艾伦？ 我任何人也不是，同时也是任何人。我是旷世催眠术师，催眠术师什么都知道。小姐你迷路了，你出自自己的心愿误入到这里，这没事，但是呆久了…… **此处有数字标记「134」** 差不多该回去自己所属的地方了，如果不你就再也回不去了，艾伦的脸都想不起来，一生被关在这里，如果不想这样就把我杀了，要回到原来的地方不得不流血。当然，如果你想这样就呆在这吧，回去好还是留下来好，自己决定吧）

  ><img src="manga-LOSTGIRLS-2-138-134.png" alt="134" width="40%">
  ><img src="manga-LOSTGIRLS-2-139-回不去了.png" alt="回不去了" width="40%">
  
- 动画台词：……我是任何人又不是任何人，而且催眠术师无所不知（亮出5把印着三笠脸的刀子），你是出于自愿来到这座迷宫的，因为**无法接受艾伦死亡的事实**，从而**自己创造出，这个新世界**，可是，无论你在哪个世界，**你都无法阻止艾伦死亡的结局**（变成三笠的声音），那是因为艾伦本身就抱着死亡的冲动，不管你再怎么保护他，死亡都一定会降临到他身上，如果你觉得我说谎了，自己去确认吧，**只不过你必须杀了我才能前往**，你必须变得坚强，回到原来的世界才行。……（三笠：你为什么要阻止我，我仅仅想和艾伦在一起而已，为什么）没有办法，世界就是这么残酷。

  ><img src="anime-ova-Lost Girls Lost in the Cruel World-1803-镜男.png" alt="镜男" width="40%">

- 三笠：为什么要妨碍我？因为世界是残酷的

然后，米卡莎像现实世界里一样爆发了力量，扎了镜男，找到阿尔敏，阿尔敏说热气球失去控制，艾伦推开阿尔敏自己撞上墙壁。三笠震惊，镜头接回真实世界。

manga-LOSTGIRLS-2-162：「……又从这里开始……」呼应了前面蝴蝶所说的「如果你不接受这个现实的话，就重新来过吧，从你想要的地方重新开始」。
  ><img src="manga-LOSTGIRLS-2-162-又从这里开始.png" alt="又从这里开始" width="40%">

本集最后的台词「不管艾伦去哪里，我都想待在他的身边」，呼应了镜男说的「自己去确认吧」。不知能否这么总结这集，三笠在现实中失去艾伦，痛苦到逃到另一个（想象的可能）世界，却（被神秘力量阻碍）经历更早艾伦的死亡，又回到现实，在现实世界接受了艾伦的死，意外的是，现实世界里艾伦还没死。

**疑惑**：
- 「无论你在哪个世界，你都无法阻止艾伦死亡的结局」这句台词在当下剧情点会让人摸不着头脑，看完巨人，我们得知这是一个铺垫。但是，这里的剧情是理解为元层次的表现，还是理解为故事内剧情呢？
- 如果把镜男的话当作事实接受，我们知道这个世界是三笠无法接受艾伦死掉的事实，自己创造出的，但她却不能创造出一个艾伦不死的世界。为什么？做出这个决定论预言的人是谁？镜男是谁？尤米尔？谏山创？为什么用三笠的声音？

ED的歌词富有深意 [TVアニメ「進撃の巨人」Season 1前期ノンクレジットED｜日笠陽子「美しき残酷な世界」](https://www.youtube.com/watch?v=eN_rq3FvJUs)，[翻译参考](https://home.gamer.com.tw/artwork.php?sn=5164105)。
> 嗚呼ボクたちは　この強さ　弱さで
> 
> 啊啊我們究竟　要用這份堅強、軟弱
> 
> 何を護るのだろう　もう理性など
> 
> 來守護些什麼呢　若是理性之類的
> 
> 無いならば
> 
> 已蕩然無存

## 第10话 - 左手的下落 左腕の行方

anime-09-2057:这里的台词强调了记忆，这在后面得到解释，并且说了之后克鲁格会说的台词：如果你想拯救三笠，阿尔敏……
> <img src="anime-ep09-2057-他们的记忆拯救阿尔敏三笠.png" alt="黑影" width="40%">

## 第12话 - 偶像 偶像
  
manga-3-158：艾伦还控制不了变身，失去控制，攻击三笠，背景中有奇怪的两个黑影
> <img src="manga-3-158-黑影.png" alt="黑影" width="40%"> <img src="manga-3-158-黑影2.png" alt="黑影2" width="40%">

## 第13话 - 伤 傷

manga-3-163 | anime-ep12-0412：三笠的脸被刀划破，这在漫画中容易被误解为溅起的飞石造成，但是动画表明并不是这样。动画镜头中是一个慢动作，周围的石头都在慢慢移动，这时伴随刀声，一道快速的刀影划过（[动画疯0412](https://ani.baha.tw/3506/04_12)），结合这集标题这里的刀伤应该有特殊用意。
><img src="manga-3-163-2-伤.png" alt="manga-3-163-2-伤" width="30%"> <img src="anime-ep12-0412-三笠伤痕.png" alt="三笠伤痕" width="30%"> 

## 第45话 - 追赶者 追う者

manga-11-123-头疼：艾伦被夺走，三笠头疼。台词仍是：又是这样吗
> <img src="manga-11-123-头疼.png" alt="头疼" width="40%">

## 第62话 - 罪 罪

anime-ep43-1633：李维问三笠有没有经历过突然觉醒的体验，三笠回答有。

<img src="anime-ep43-1633-觉醒.png" alt="某种东西的奴隶" width="40%"> <img src="anime-ep43-1633-觉醒2.png" alt="某种东西的奴隶" width="40%">

anime-ep43-0206：罗斯家族二人触碰艾伦，艾伦看到老爹杀人的记忆，老爹视角里自己吃老爹的记忆。（两个罪人）希斯特里亚恢复了被弗丽达消除的记忆。

<img src="anime-ep43-0206-接触.png" alt="某种东西的奴隶" width="40%">

## 第69话 - 友人 友人

anime-ep47-1719 manga-17-124 肯尼：

<img src="anime-ep47-1719-某种东西的奴隶.png" alt="某种东西的奴隶" width="40%">

```
今ならヤツのやったこと　わかる気がする。俺が見てきた奴ら　みんな　そうだった　酒だったり　女だったり　神様だったりもする　一族　王様　夢　子供　力　みんな　何かに酔っ払ってねえと　やってられなかったんだな　みんな　なにかの奴隷だった　あいつでさえも　お　お前は何だ？　英雄か？
```
现在我感觉我能理解他做的事了。我见过的人们，都是那样，不管是酒（？）、女人（罗德·雷斯）、神（教徒），族人（肯尼爷爷）、国王（？）、梦想（肯尼部下）、孩子（妹妹？）、力量（肯尼），每个人都陶醉于某种东西，否则就活不下去。大家都是某种东西的奴隶，就连他（乌利王）也是。你，你呢？（问李维）成为英雄吗？

这句话在第三季出现，却貌似概括到了很多关键人物的剧情。把“大家都是某种东西的奴隶”推广到这里没提到的人物：

- 艾伦：自由
- 三笠：对艾伦的爱
- 阿尔敏：大海？
- 尤弥尔：对弗里兹王的爱
- 艾尔文：真相

（这句话似乎有助于理解尤弥尔的解脱，首先尤弥尔没有完全死掉，活在道路里，是虫子的能力+她有留恋的结果，换成这里的说法就是对某种事物的陶醉，是某种事物的奴隶，这种不释怀的执着是道路（坐标）形成的必要条件。问题是最后艾伦解脱了吗？在和阿尔敏的对话中，艾伦说希望三笠10年想着她，这是否也是一种执着？反过来，三笠10年守着艾伦意味着10年内也没有解脱？）

## 第85话 - 地下室 地下室

阿尔敏忘记了自己继承巨人的事，反映了继承巨人会造成记忆丧失的特性。此处强调贝尔托特变巨人之后的时间是动画独有内容。

> <img src="anime-ep56-0316-记忆.png" alt="克鲁格" width="50%">
> 
## 第88话 - 进击的巨人 進撃の巨人

manga-22-68：克鲁格的小时候故事。

> <img src="manga-22-68-克鲁格.png" alt="克鲁格" width="50%">

manga-22-73：尤弥尔的诅咒，这里严谨点理解的话，只是说一定会少于尤弥尔的13年，并且会越来越虚弱，并非是一定能活到第13年。

> <img src="manga-22-73-尤弥尔的诅咒.png" alt="尤弥尔的诅咒" width="50%">

manga-22-76：关于道路的内容，「有时候，记忆和谁的意志也会以同样的方式通过道路」这里呼应之后格里沙在地下说的看见记忆的设定，但这个「有时候」说法似乎不像是能操控的，更像是不可控的某些条件下。

> <img src="manga-22-76-道路.png" alt="道路" width="50%">
 
>  <img src="manga-22-77-道路.png" alt="道路" width="50%">

anime-ep58：通过后面的原理，我们知道，克鲁格此时接受到了格里沙的记忆。

> <img src="anime-ep58-2240-克鲁格的话.png" alt="克鲁格的话" width="40%">

## 第90话 - 前往城墙的另一端 壁の向こう側へ

anime-ep59-1332: 亲吻希斯特里亚的手，艾伦不想牺牲希斯特里亚，要保护她。然后接触到手时，艾伦看到了一些记忆。
> <img src="anime-ep59-1332-不想牺牲希斯特里亚.png" alt="克鲁格的话" width="40%">

其中知道了格里沙对弗丽达·雷斯说的台词：...快去杀了正在攻入城墙的巨人，在我的妻子，孩子，民众被吃之前。这段台词里有孩子，而实际上他的孩子没有被吃，说明格里沙此时并不知道之后发生了什么，只知道了巨人破坏了墙壁，家人有危险。

> <img src="anime-ep59-1400-阻止.png" alt="阻止" width="40%">

- 积雪融化时（851春），玛利亚墙内巨人清理干净
- 托洛斯特区遭到攻击一年后(850+1 = 851)，人们返回故乡
- 超大巨人攻击6年后（845+6 = 851），调查兵团出墙

## 第91话 - 大海的另一端 海の向こう側
manga-23-7：法尔科看着鸟，对鸟说这里很危险，非走吧。这里和法尔克变成会飞的巨人，以及和艾伦是否有实质上的联系？
> <img src="manga-23-7-鸟.png" alt="法尔克" width="40%">

anime-ep60：这个姿势和尤弥尔相似。
> <img src="anime-ep60-0000-法尔克.png" alt="法尔克" width="40%"> <img src="anime-ep37-1647-尤弥尔.png" alt="法尔克" width="40%">

anime-ep60：法尔克犯迷糊。这里的台词明显是描述作为调查兵团的梦，可推测法尔克看到了作为调查兵团的尤弥尔的梦。这从侧面应证了，**巨人继承者可能在继承之前就看到之前继承者的记忆**。
> <img src="anime-ep60-0142-梦到了.png" alt="法尔克" width="40%">

## 第106话 - 义勇兵 義勇兵

manga-26-179：阿尔敏看到了贝尔托特的记忆。
> <img src="manga-26-179-贝尔托特的记忆.png" alt="各个回忆" width="80%">

## 第110话 - 虚伪的人 偽り者

三笠在和露易泽对话完后，出现了头疼，看到了小时候杀人时的艾伦。

> <img src="anime-ep70-1204-luize.png" alt="luize" width="40%">

## 第115话 - 支え 支持
回过头看，为什么艾伦和吉克谈妥的时候，不直接接触呢？尽管两人目的不同，但这里的发动条件和最终发动时的条件没什么不同，为什么要经历两次突袭行动后才接触呢？

> <img src="manga-29-10-信赖的人.png" alt="信赖的人" width="40%"> <img src="manga-29-23-先不接触.png" alt="先不接触" width="40%">

可能这里是一个铺垫，吉克不是发动者，所以需要充分信任艾伦和自己想法一样才行。能否这样说，吉克想要伪装成自己已经死亡，然后在小岛上两人发动断子绝孙，可为什么不一回到小岛就接触？把脊髓液放到酒里等这些操作是为了什么？

## 第119话 - 兄与弟 兄と弟

manga-30-19-等等：艾伦阻止了吉克吼叫，然后法尔克哥哥拉着法尔克出现。这里非常奇怪，应该是艾伦某个目的。先随便写个猜想防止遗忘，艾伦之前看到过法尔克出现在未来，有关键作用，发现此时法尔克可能会被变，很恐慌。

> <img src="manga-30-19-等等.png" alt="法尔克" width="40%">

## 第120话 - 刹那 刹那

manga-30-62-63：艾伦脑袋接触到吉克时看到的内容。盘点一下，**全是进击的巨人或是始祖巨人的继承者的第一人称记忆画面**。包括未来艾伦的记忆（小孩，未来的希斯特里亚），艾伦过去的记忆（幼时三笠），芙丽达的记忆（照镜子，幼时希斯特里亚），格里沙的记忆（妹妹），克鲁格（踢人下去，第二张右下方最大的是不是也是克鲁格小时候的记忆？）。

> <img src="manga-30-62-各个回忆.png" alt="各个回忆" width="80%">
> 
> <img src="manga-30-63-各个回忆.png" alt="各个回忆" width="80%">

动画的内容：

> <img src="anime-ep78-1530-接触01.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触02.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触03.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触04.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触05.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触06.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触07.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触08.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触09.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触10.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触11.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触12.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触13.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触14.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触15.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触16.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触17.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触18.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触19.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触20.png" alt="各个回忆" width="30%"> <img src="anime-ep78-1530-接触21.png" alt="各个回忆" width="30%">

其中有一个蒸桑拿的情景，这似乎对应着NHK在2023年10月23日播放的「仕事の流儀 エレン・イェーガー」中提到艾伦从讨厌桑拿（サウナ）到喜欢桑拿，这似乎是原作完全没有提到的一个内容，这里特地添加。第33卷的スクールカースト中也有这样一个桥段，但是人物站位和动画里的这张图并不对应。考虑到这里是有胡茬的莱纳，李维，让等人，如果本篇中存在这样的场景，能在哪里呢？

> <img src="仕事の流儀 エレン・イェーガー.png" alt="各个回忆" width="45%"> <img src="manga-32-190-桑拿.png" alt="桑拿忆" width="45%">

还有两个人脸在本篇中没有出现过。后两者是21卷到34卷在卷尾添加的「スクールカースト」neta小故事，用和本篇相同的人名，个性，貌似架空在美国学校（霸凌之类的“等级”事件）发生的故事。其中三笠是哥特装扮，阿尔敏是geek模样。虽然是搞笑漫画，但其中neta了不少本篇中的桥段。并且在34卷的最后一篇中提到这是巨人消失后的100年，明确地指明了这个系列和主线在同一个世界。

> <img src="manga-34-243-进击等级学校.png" alt="各个回忆" width="40%"> <img src="manga-34-243-进击等级学校2.png" alt="各个回忆" width="40%">

能在记忆碎片中看到不知道是neta还是有严格的原因。难道这个系列里的爱伦是进击的巨人继承者？这不就和巨人之力消失矛盾了嘛。


## 第121话 - 未来的记忆 未来の記憶

这部分的综合讨论部分放在解读中。

现在看来标题也许是个巨大的剧透。未来的记忆，意思是某个或某些主体在未来产生的记忆，而非未来本身，这两者有很重要的不同。更具体地说，如果不存在主体，未来依旧存在，而未来的记忆的存在必须依靠某些主体在未来存在。

manga-30-85：艾伦这句台词如果如字面意思，那么会产生问题，因为艾伦和吉克是从第三人称视角来观看整个场景的，而非格里沙的第一视角，不能说是格里沙的记忆，而是记忆里的世界。

> <img src="manga-30-85-老爸的记忆.png" alt="老爸的记忆" width="40%">

但这里可能是表现手法受限。让我们假设艾伦和吉克看到的场景确实是第一人称的，这会和“艾伦是通过看格里沙的脸让格里沙看到自己的记忆从而意识到什么”理论矛盾，因为这时艾伦在第一人称不可能能看到格里沙的脸。所以，排除掉夸张表现手法，而应当把艾伦的站位等信息全部当作有意义的信息。

艾伦的视线正好看到吉克，暗示实现互动的原理是通过艾伦的视线。即格里沙此时看到了此时艾伦的记忆。

> <img src="manga-30-95-看到吉克.png" alt="看到吉克" width="40%"> <img src="anime-ep79-1037-对视.png" alt="对视" width="40%">

anime-ep79-1218: 镜头做成两人对视的样子，通过后来的“未来的记忆”可以知道此时格里沙看到了自己的脸。

> <img src="anime-ep79-1218-对视.png" alt="对视" width="40%">

manga-30-117: 逐字分析，不是未来，也不是自己未来的记忆，而是未来的继承者的记忆，换句话说格里沙看不到自己未来的记忆，但能看到艾伦的记忆。可为什么能看到？

> <img src="manga-30-117-进击的巨人的特性.png" alt="进击的巨人的特性" width="40%">

manga-30-124-经典互动：什么是记忆？应该不仅包含视觉，还有听觉、嗅觉、味觉、触觉和心情、思想。在这个基础上，这里不仅仅是看到艾伦看自己的侧脸，还因为体验到了艾伦整个愤怒的情感和冲动。

> <img src="manga-30-124-经典互动.png" alt="经典互动" width="40%">


manga-30-125：这里格里沙的表情和之后授勋式上艾伦的表情一致，可知就是在此时，格里沙看到了艾伦未来的记忆。

> <img src="manga-30-125-表情.png" alt="经典互动" width="40%">

manga-30-128-129：为什么这里要插入希斯特里亚的手。我觉得有两种可能性，一种是说此时得格里沙看到了授勋式上艾伦的记忆；第二种是说艾伦在授勋式上看到了此时的记忆。从第一人称角度来说，第一种反而可能性更大。

> <img src="manga-30-128-希斯特里亚的手.png" alt="希斯特里亚的手" width="40%"> <img src="manga-30-129-希斯特里亚的手.png" alt="希斯特里亚的手" width="40%">

manga-30-130：为什么不给我看全部，这句台词值得注意，似乎意味着艾伦能够主动把自己的记忆传给格里沙，从而有选择地没让格里沙看到自己母亲被吃的记忆。但这个传递记忆的能力的条件是什么，是始祖进击王室到手后的能力吗？

“艾尔迪亚这样就真的得救了吗？”可以看出，艾伦此时的心情和意志也随着记忆传递给了格里沙，艾伦确实是想让希斯特里亚等艾尔迪亚人活下去。

> <img src="manga-30-130-为什么不给我看全部.png" alt="为什么不给我看全部" width="40%">

manga-30-132,135：

> <img src="manga-30-132-亲手.png" alt="亲手" width="40%"> <img src="manga-30-135-亲手.png" alt="亲手" width="40%">

manga-30-139：还没看到父亲被我吃地记忆。

> <img src="manga-30-136-还没看到父亲被我吃地记忆.png" alt="还没看到父亲被我吃地记忆" width="40%">

manga-30-139：这句话没有什么可怀疑的。艾伦直接说了，**自己亲吻希斯特里亚手的时候，通过父亲（看到未来自己的记忆）的记忆看到了未来自己的记忆，那个景色（地鸣）**。动画版的台词基本一样，只是改成了“我通过老爸的记忆看到了自己的未来”，没有像漫画一样说“看到了未来的自己的记忆”。

> <img src="manga-30-139-依靠父亲看到未来.png" alt="依靠父亲看到未来" width="40%">

## 第122话 - 从两千年前的你 二千年前の君から

manga-30-145: 插叙了希斯特里亚看书的回忆，补充解释了希斯特里亚的人设。尤米尔是个对他人善良的人，所以希斯特里亚也一直这样。之后，在扮演尤米尔的尤米尔的帮助下，更加自我，任性地救了艾伦，成为“坏女孩”。而艾伦帮助尤米尔，摆脱奴隶身份，自己决定。这里补充，穿起来了4个人的行为动机。

> <img src="manga-30-145-像尤米尔一样.png" alt="像尤米尔一样" width="40%">

manga-30-146: 割舌头，大概率尤米尔也被割了舌头，无法说话。

> <img src="manga-30-146-割舌头.png" alt="割舌头" width="40%">

manga-30-169: 花瓣有9片，和九大巨人数量一样。不知有什么关系。

> <img src="manga-30-169-花瓣.png" alt="花瓣" width="40%">

manga-30-180: 艾伦说出这样的台词，意味着艾伦了解尤米尔的身世，他是如何知道的呢？是否是接触希斯特里亚时就看到了？

> <img src="manga-30-180-两千年.png" alt="花瓣" width="40%">


## 第127话 - 终末之夜 終末の夜

> <img src="manga-32-5-让的妄想.png" alt="让的妄想" width="40%"> <img src="manga-32-5-让的妄想2.png" alt="让的妄想2" width="40%">

## 第130话 - 人类的黎明 人類の夜明け

anime-ep87-0447：动画版增加了插叙，众人第一次到海对岸地场景，以及艾伦提前看到小孩，艾伦和三笠在上坡上的场景。这句台词说明能看到其他继承者继承巨人之前的记忆。因为冰淇淋的记忆是格里沙被注射之前的记忆。

现在我的markdown中有很多形如
> <img src="anime-ep87-0447-看到冰淇淋.png" alt="看到冰淇淋" width="40%"> <...>
的格式
请帮我写个脚本自动把这些全部替换为折叠模式<details>的折叠模式，并且summary 中写alt中的内容


manga-32-145-147：画面上是众人乘坐的船，天上有白鸟，接着艾伦的独白。可能是暗示艾伦能通过鸟看到这里的景象？艾伦问自己，是从哪里开始的，紧接着一些回忆。

> <img src="manga-32-145-各个回忆.png" alt="各个回忆" width="80%">

manga-32-146：艾伦问自己，是从哪里开始的，紧接着一些回忆。
- 树下 第三视角
- 🐖 尤米尔的第一视角
- 格里沙 艾伦的第一视角
- 亲手 第三视角

> <img src="manga-32-146-各个回忆.png" alt="各个回忆" width="80%"> 

manga-32-147：

> <img src="manga-32-147-各个回忆.jpg" alt="各个回忆" width="80%">

- 亲手 第三视角
- 李维 艾伦第一视角
- 火车上 艾伦第一视角
- 皮克拿枪指着自己 艾伦第一视角
- ※　米卡莎 艾伦的第一视角
- ※　希斯特里亚 艾伦(？)第一视角
- ※　法尔克 鸟的视线
- 米卡莎来马莱见面 艾伦的第一视角
- 老爹侧脸 老爹记忆世界时艾伦的第一视角
- 吉克抓住自己脑袋 艾伦的第一视角
- 被打的阿尔敏 艾伦的第一视角
- ※　超大巨人破坏墙壁后的贝尔托特 第一视角or第三视角
- 爷爷 艾伦的第一视角
- ※　韩吉 ？的第一视角

对于第三视角画面，我觉得可以理解为像进入格里沙记忆世界一样，进入艾伦自己的记忆世界，就能从第三视角来看。（艾伦大概也多次徘徊在自己的记忆世界里寻找答案吧）

对于其他的记忆，※标注的画面都很重要，需要认真分析。

## 第131话 - 地鸣 地鳴らし

出现了尤弥尔的身影 manga-33-31-尤弥尔的身影

> <img src="manga-33-31-尤弥尔的身影.png" alt="尤弥尔的身影" width="40%">

艾伦说，这就是自由。然后转头看阿尔敏。这里铺垫了艾伦和阿尔敏在道路中的对话，根据后面可以推测是艾伦删除了阿尔敏的记忆。manga-33-43，manga-33-44：

> <img src="manga-33-43-到达自由和阿尔敏.png" alt="到达自由和阿尔敏" width="40%"> <img src="manga-33-44-到达自由和阿尔敏.png" alt="到达自由和阿尔敏" width="40%">

## 第137话 - 天与地的战斗 天と地の戦い

尤米尔在这里出现，是什么意思
> <img src="manga-34-12-尤米尔.png" alt="尤米尔" width="40%">

这里，虐杀人类，是尤米尔的意志，而不一定是艾伦的意志。
> <img src="manga-34-31-尤米尔的意志.png" alt="尤米尔的意志" width="40%">

## 第xx话 - 

阿尔敏说，“再让我”问一遍，你哪里自由了。此处的“再”是相对哪次的？

## 第137话 - 巨人 巨人

manga-34-130：吉克被砍头，地鸣停止，证明王室对维持地鸣的不可或缺。
> <img src="manga-34-130-地鸣停止.png" alt="地鸣停止" width="40%">
> 
anime-终part2-004333：艾伦在此出现，动画独有镜头接着希斯特里亚接生的场景。有一种可能性出生的孩子继承了之前死去的吉克的长毛巨人，这个想法十分合理。但如何利于解释其他内容还不清楚以及她如何能在巨人之力“消失”后继续保留，值得研究。
> <img src="anime-终part2-004333-生孩子.png" alt="生孩子" width="40%">

## 第138话 - 漫长的梦 長い夢

manga-143：米卡莎想起艾伦的讨厌，竟然那是最后一面，难以接受而头疼。
> <img src="manga-143-艾伦死头疼.png" alt="艾伦死头疼" width="40%">
><img src="anime-终part2-004422-头疼.png" alt="头疼" width="40%">

manga-34-170：艾伦又活过来，和大家打到一起。三笠又头疼。这里第一刻三笠想到的是树下睡着的艾伦，之后才是二人小屋的世界。

> <img src="manga-34-170-头痛1.png" alt="头痛1" width="40%">
> <img src="manga-34-170-头痛.png" alt="头痛" width="40%">

manga-34-175：这个世界，是在山坡上回答「家人」时如果给出不同回答分歧后形成的世界。

> <img src="anime-终part2-005310-逃亡生活.png" alt="逃亡生活" width="40%">

艾伦说，无论牺牲希斯特里亚重复纷争历史，还是屠杀岛外的人，他都做不到，于是他选择了和三笠私奔，度过4年余生。反向推理，13年的寿命，山坡上说话应该是第9年，845是第一年，第九年是853年，到854年春有点短，认为从艾伦消失到大战的时间在一年以内的话，勉强说的过去。认为这里和真实世界的时间是同步的。所以作为平行世界的同时间剧情理解较自然，但会有其他的挑战，此处略。
><img src="manga-34-175-小屋线.png" alt="小屋线" width="40%">

manga-34-176：艾伦说「拜托忘掉我」
><img src="manga-34-176-忘掉我.png" alt="忘掉我" width="40%">

manga-34-179：接着小屋世界艾伦的「拜托忘掉我」，三笠回答「做不到」。这是两个世界的两个三笠做出了相同的回答，仅仅是镜头放在一起呼应，还是同一个三笠在脑中模拟了一个可能世界后又回到现实世界？以及造成观众看到这个小屋世界的是艾伦还是三笠，还是其他人？这些是关于理解结尾的关键问题。
><img src="manga-34-179-做不到.png" alt="做不到" width="40%">

manga-34-185：第138话（漫长的梦境，長い夢）的第45页（此话一共46页，第46页是接吻画面），三笠说「艾伦，一路小心」。呼应了「第1话 给两千年后的你」，两处数字连起来的结果「13845」。
><img src="manga-34-185-一路走好.png" alt="一路走好" width="40%">

尤米尔笑了。
><img src="manga-34-186-笑.png" alt="笑" width="40%">

## 第139话（最終話） - 朝着那座山丘上的树 あの丘の木に向かって

### 阿尔敏和艾伦的对话

【第一段】：**艾伦的目的是把阿尔敏等塑造为讨伐艾伦的英雄。** 阿尔敏拿戴巴家族作类比（戴巴家族用巨人之力杀掉巨人，成为英雄，保护艾尔迪亚人？现在，阿尔敏等用巨人之力杀掉艾伦，成为英雄，保护帕拉迪岛）漫画中艾伦紧接着说因为会死80%的人类，岛外无法报复帕拉迪岛。动画中删去了这部分。

【第二段】：**巨人之力的存在是因为尤米尔2000年来一直服从着弗利兹王。** 尤米尔爱着弗利兹王是束缚她2000年的原因。她一直寻求着帮她解脱的人，那就是三笠。漫画比动画多一个「围巾」的分镜，这个分镜和 manga-12-169 不一致，也和 manga-34-237 不一致。

><img src="manga-34-195-三笠.png" alt="三笠" width="40%">
><img src="anime-终part2-005956-三笠.png" alt="三笠" width="40%">
manga-12-169 和 manga-34-237：
><img src="manga-12-169-三笠.png" alt="三笠" width="40%">
><img src="manga-34-237-三笠.png" alt="三笠" width="40%">

最大可能是 manga-34-237 之后鸟飞起来后，「给我围上围巾，谢谢」这句话时的分镜，只不过观众没有看到。如果是这样，艾伦能看到是因为看到了鸟的记忆？动画删掉此处又是为何？

艾伦说三笠做了什么，他不知道，只知道他做的一切是 **为了** 到达那个结果。明艾伦「看」到了结果，但没看到艾伦砍自己。结合希斯特里亚的独白，看到的结果是**巨人之力消失之后的世界。**

之后阿尔敏说：这就是你在授勋式上看到的未来。艾伦没有否定。始祖力量让艾伦脑袋混乱，「过去」「未来」同时存在。那一天，贝尔托特 **不该死** ，让巨人朝着妈妈卡露拉过去的是……（我）。

><img src="manga-34-197-不该死.png" alt="不该死" width="40%">

这句话说明，始祖力量能控制不同时间上的巨人，但 **不该死** 是谁定下的呢？ **为了到达那个结果** 是艾伦对多种结果的权衡结果，还是别人让艾伦不得不到达那个结果？ 如果是前者，艾伦是自由的，但也是时间悖论的，毕竟艾伦自己也经历过没有始祖力量的时间。如果是后者，那尤米尔自然是最可能决定一切的那个人，艾伦只是感觉能控制一切，感觉能做出选择的决定论奴隶。如何解释这里的对话，十分关键。

【第三段】：艾伦对阿尔敏说“正如你说的”，我是自由的奴隶。阿尔敏什么时候对艾伦说过？是指终章中到达艾伦背上时，阿尔敏对艾伦说的吗？如果是的话，此时艾伦和阿尔敏的对话发生在船上的一瞬，早于阿尔敏的话。

这句话**想让三笠在自己死后至少想自己10年** 动画在这一段有做改动，添加了：

  anime-终part2-010415
  ><img src="anime-终part2-010415-无数次.png" alt="无数次" width="40%">

  ><img src="anime-终part2-010605-想做.png" alt="想做" width="40%">

  ><img src="anime-终part2-010632-笨蛋.png" alt="笨蛋" width="40%">

  似乎还是关于艾伦矛盾的叙述的演出效果，一方面觉得自己无可奈何被决定着怎么做，一方面又觉得自己确实想这么做。对解答之前的疑问没有什么帮助。

二人对话之后紧接着在船上的剧情，可以确定对话发生在这时候，并消除了阿尔敏的记忆。一只鸟飞过，仿佛暗示着或者实质上就是艾伦。

manga-34-207-船上：

><img src="manga-34-207-船上.png" alt="船上" width="40%">

### 大家想起被抹去的记忆

manga-34-211：这两句台词十分令人疑惑：

><img src="manga-34-211-想起了阿尔敏.png" alt="想起了阿尔敏" width="40%">
  - 三笠：「阿尔敏的记忆 **也** 恢复了吧，就是 **艾伦来见我们的时候**」 暗示三笠也失忆过？但阿卡曼能被篡改记忆吗？
  - 艾伦来见我们的时候是什么时候？好像和阿尔敏一个人在船上不太符合？
  - 阿尔敏：我都听他说了，三笠你带来的结果就是让巨人之力从世上消失
  - 观众看到的对话中，艾伦并不知道也没有告诉阿尔敏结果是什么，和这句话矛盾

manga-34-213：大家也想起来，只有皮克没有和艾伦说过话。
  ><img src="manga-34-213-大家想起.png" alt="大家想起" width="40%">
  ><img src="manga-34-214-皮克没说.png" alt="皮克没说" width="40%">

  如果每个人是单独说的，三笠怎么知道是「见我们的时候」？如果是一起说的，那观众看到的和阿尔敏的单独对话是怎么回事，为什么皮克不在场？「见我们的时候」是哪个时候以及当时究竟是怎么说的，作者刻意隐藏了这部分。

  或者仅仅把这里的「也」当作是相对之后其他人来说的，尽管其他人的镜头在之后才给出，同理，「见我们的时候」=「见我们的各个时候」。但这样解释会非常违背说话的正常直觉。

### 三笠对尤米尔说

><img src="manga-34-225-尤米尔.png" alt="尤米尔" width="40%">

- 在我的脑袋里窥视：似乎和头疼联系起来比较自然。
- 三笠：被夺走的生命（尤米尔你的生命）已经不能回来，但正因为你生下的生命（你的女儿），才有了我（所有艾尔迪亚人）。画面出现了「另一个结果」弗利兹王被矛插死，尤米尔活了下来。这是否是尤米尔一直渴望的另一个结果？这种渴望通过三笠得到了实现。

### 希斯特里亚的独白

manga-34-227：战争时出生的孩子满三岁。

><img src="manga-34-227-三岁.png" alt="三岁" width="40%">

manga-34-230：漫画这里比动画说的更直白一些，艾伦在之前告诉了希斯特里亚他看到的未来，艾尔迪亚人和世界某一方消失之前战争都不会结束。注意这个未来的时间已经超过了巨人之力消失的时间。

<img src="manga-34-230-艾伦告诉希斯特里亚.png" alt="艾伦告诉希斯特里亚" width="40%">

### 片尾

manga-34-235-墓碑：根据日本网友的推理和在作品中的多次验证，把日语的每个片假名旋转180°就能得到进击的巨人世界观里的文字，所以这段碑文的内容是：
- 「最愛の　あなた　永久にここで　眠りにつく 854」

<img src="manga-34-235-墓碑.png" alt="墓碑" width="40%">

anime-终part2-012220：大家在三年后，857年，春天来看艾伦，之后一共出现了8次雪天，再到春天（865年春），（865春-854春）过了完整的11年，三笠和男人、小孩出现（说明在第11年期间生的小孩），符合艾伦的期待，完整的10年单身。
><img src="anime-终part2-012220-十年后.png" alt="十年后" width="40%">

## 最后的进击 电影

新镜头 三人在过斑马线时，远处的山头上是那棵参天大树。说明此处是帕拉迪岛。呼应着艾伦脑袋接触吉克时看到两个人的脸，他们也是艾尔迪亚人。但具体原理仍然是谜团。

> <img src="manga-34-243-进击等级学校2.png" alt="各个回忆" width="40%">
"""

converted_markdown = convert_markdown_images_to_details(markdown_input)
print(converted_markdown)
## 指令3のスペシャルヒント

まずは、訓練３でやったことを思い出してください。

表示名に色がつくのは、ソースコード内で  
&lt;font color=<font color="lime">'</font><font color="red">red</font><font color="lime">'</font>&gt;[表示名]&lt;/font &gt;
という指定が入っているためです。

この<font color="red">red</font>に入る文字列を指定しているのは、

&lt;input class="form-check-input" type="radio" name="color" id="radios1" value='<font color="red">red</font>' checked&gt;  
&lt;label class="form-check-label" for="radios1"&gt;赤&lt;/label&gt;  
のところで、この<font color="red">red</font>をハッキングできるのは訓練３で学んだとおりです。

<font color="red">red</font>を単純に<font color="cyan">&lt;script&gt;alert('message');&lt;/script&gt;</font>にしても、    

&lt;font color=<font color="lime">'</font><font color="cyan">&lt;script&gt;alert('message');&lt;/script&gt;</font><font color="lime">'</font>&gt;[表示名]&lt;/font &gt;
となり、全体が <font color="lime">'</font> に囲まれます。  
<font color="lime">'</font>文字列<font color="lime">'</font>は<font color="lime">「</font>文字列<font color="lime">」</font>と同じで、この囲まれた状態だと不正コードは全体が文字列とみなされます。
もともとのソースにある<font color="lime">「</font>に当たる部分を<font color="lime">」</font>で閉じる必要があります。もちろん&lt;は&gt;で閉じるわけですが…


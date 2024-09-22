## 進度

### types

> 截自：https://wadehuanglearning.blogspot.com/2019/05/commit-commit-commit-why-what-commit.html  
> feat: 新增/修改功能 (feature)。  
> fix: 修補 bug (bug fix)。  
> docs: 文件 (documentation)。  
> style: 格式 (不影響程式碼運行的變動 white-space, formatting, missing semi colons, etc)。  
> refactor: 重構 (既不是新增功能，也不是修補 bug 的程式碼變動)。  
> perf: 改善效能 (A code change that improves performance)。  
> test: 增加測試 (when adding missing tests)。  
> chore: 建構程序或輔助工具的變動 (maintain)。  
> revert: 撤銷回覆先前的 commit 例如：revert: type(scope): subject (回覆版本：xxxx)。

* 2024/09/17
	1. feat: 完成切板(包括工具列按鈕、選單和側邊攔的捲動與布局)

* 2024/09/20
	1. feat: layer list scroll bar
	2. feat: layer sort (按住後拖曳，只在垂直方向步進式交換(改 index))

* 2024/09/22
	1. feat: layer focus (single click a layer)
	2. feat: layer button 功能 (new full layer, new clip layer, delete selected layer)
	3. feat: layer id (用以辨識實體不同但名稱相同的 layer)
	4. feat: layer rename (double click a layer)
	5. feat: layer icon (full or clip，改用 \[f\] 和 \[c\] 之前綴代替)
	6. feat: full layer display (on workspace) 
	7. feat: workspace move (wheel)
	8. feat: workspace scale

## 待辦

- [ ] 直長型視窗的布局(theme 新增不同部局並支援各 component 的 top/bottom、left/right)
- [ ] tiny view display

- [ ] workspace move (drag)
- [ ] clip layer display (on workspace)
- [ ] clipping layer control points and edit method

- [ ] file read/write

- [ ] basic render
- [ ] outline render
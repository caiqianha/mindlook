<map version="1.0.1">
<!-- Synthetic FreeMind / Freeplane sample for Mindlook. 合成示例，仅用于演示。 -->
<node TEXT="产品发布计划 Product launch plan" ID="ID_1" CREATED="1700000000000" MODIFIED="1700000000000">
<font NAME="SansSerif" SIZE="16" BOLD="true"/>
<richcontent TYPE="NOTE"><html><head></head><body><p>这是根节点的备注。<b>FreeMind</b> 的备注用 richcontent 存放。</p><p>Notes on the root node, stored as rich content.</p></body></html></richcontent>
<node TEXT="目标 Goals" POSITION="right" ID="ID_2">
<icon BUILTIN="full-1"/>
<node TEXT="Q4 上线 ship in Q4" ID="ID_3"><icon BUILTIN="button_ok"/></node>
<node TEXT="首月 1 万用户 10k users in month one" ID="ID_4"><icon BUILTIN="flag-green"/></node>
<node TEXT="NPS ≥ 40" ID="ID_5"><attribute NAME="owner" VALUE="Lin"/></node>
</node>
<node TEXT="工作流 Workstreams" POSITION="right" ID="ID_6">
<node TEXT="工程 Engineering" ID="ID_7" FOLDED="true">
<node TEXT="API 冻结 API freeze" ID="ID_8"/>
<node TEXT="性能基线 performance baseline" ID="ID_9"/>
<node TEXT="压测 load test" ID="ID_10"><icon BUILTIN="hourglass"/></node>
</node>
<node TEXT="设计 Design" ID="ID_11" LINK="https://example.invalid/design-spec">
<node TEXT="视觉稿 visual spec" ID="ID_12"/>
<node TEXT="无障碍审查 accessibility review" ID="ID_13"><icon BUILTIN="help"/></node>
</node>
<node ID="ID_14"><richcontent TYPE="NODE"><html><head></head><body><p>市场 <i>Marketing</i>（富文本标题）</p></body></html></richcontent>
<node TEXT="发布文章 launch post" ID="ID_15"/>
<node TEXT="社媒排期 social schedule" ID="ID_16"/>
</node>
</node>
<node TEXT="风险 Risks" POSITION="left" ID="ID_17">
<icon BUILTIN="messagebox_warning"/>
<node TEXT="第三方 SDK 延期 vendor SDK slips" ID="ID_18"/>
<node TEXT="人手不足 staffing gap" ID="ID_19"><richcontent TYPE="DETAILS"><html><body><p>需要再招一名后端</p></body></html></richcontent></node>
<arrowlink DESTINATION="ID_10" STARTARROW="None" ENDARROW="Default"/>
</node>
<node TEXT="里程碑 Milestones" POSITION="left" ID="ID_20">
<node TEXT="10-20 代码冻结 code freeze" ID="ID_21"/>
<node TEXT="11-05 Beta" ID="ID_22"/>
<node TEXT="11-25 GA" ID="ID_23"><icon BUILTIN="idea"/></node>
</node>
</node>
</map>

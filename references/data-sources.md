# Data Sources — 数据源配置

> 本文件定义 multi-agent-trend-ai 的所有数据源、降级顺序、速率限制与鉴权配置。
> 最后更新: 2026-06-19

---

## 1. 数据源清单

| 优先级 | 名称 | URL | 类型 | 更新频率 | 权重 |
|--------|------|-----|------|----------|------|
| 1 | 微信搜一搜 | https://weixin.sogou.com/ | 站内搜索指数 | 实时 | 0.30 |
| 2 | 微信指数 | https://search.weixin.qq.com/ | 官方热度 | 日 | 0.25 |
| 3 | 公众号热门 | https://mp.weixin.qq.com/ | 平台原生 | 实时 | 0.20 |
| 4 | 视频号热门 | https://channels.weixin.qq.com/ | 平台原生 | 实时 | 0.15 |
| 5 | PaiCoding AI 热点雷达 | https://aihot.paicoding.com/ | 跨平台聚合 | 日 | 0.05 |
| 6 | 36 氪 AI 专题 | https://36kr.com/ | 行业媒体 | 日 | 0.03 |
| 7 | 腾讯云开发者社区 | https://cloud.tencent.com.cn/developer/ | 开发者社区 | 日 | 0.01 |
| 8 | 知乎专栏 | https://zhuanlan.zhihu.com/ | UGC 社区 | 日 | 0.01 |

> 权重合计 = 1.00。在多源冲突时按权重聚合。

---

## 2. 降级顺序

```
[1] 微信搜一搜
        ↓ 失败 (超时/反爬/5xx)
[2] 微信指数
        ↓ 失败
[3] 公众号热门 + 视频号热门
        ↓ 失败
[4] 跨平台聚合源 (PaiCoding / 36kr / 腾讯云 / 知乎)
        ↓ 全部失败
[5] references/keyword-pool.md (本地库，标 "可能过期")
        ↓ 失败
[6] 返回空结果 + 引导用户提供素材 (不编造数据)
```

降级触发条件：
- 单源连续 2 次请求失败 → 标记 `source_unavailable`
- >60% 数据源失败 → 启动降级模式 `degraded_mode`，输出顶部加 `⚠️ 数据降级` 提示

---

## 3. 鉴权与速率限制

### 3.1 微信相关
- **微信搜一搜**: 无需鉴权，UA 伪装为标准浏览器
- **微信指数**: 无需鉴权，需带 `Referer: https://wx.qq.com/`
- **公众号/视频号热门**: 无公开 API，需通过 WebFetch 抓取搜索结果页

### 3.2 第三方
- **PaiCoding**: 公开站点，无限制
- **36 氪**: 公开站点，每 IP 60 req/min
- **腾讯云**: 公开站点，每 IP 30 req/min
- **知乎**: 需带 Cookie，建议 30 req/min 以内

### 3.3 环境变量（避免硬编码）
```bash
# .env (本地)
TAVILY_API_KEY=tvly-xxxxx
WECHAT_USER_AGENT="Mozilla/5.0 ..."
WECHAT_REFERER="https://wx.qq.com/"
```

> **安全声明**: 本 Skill 不收集任何 PII，密钥仅通过环境变量注入。

---

## 4. 抓取合规

- ✅ 仅做热度聚合与关键词提取
- ❌ 不存储公众号/视频号原文
- ❌ 不绕过登录墙
- ✅ 遵守 robots.txt（默认）
- ❌ 不进行高频抓取（>5 req/s 触发熔断）

---

## 5. 数据源健康检查

每 24h 自动 ping 一次所有源，更新状态表：

| 源 | 上次成功 | 状态 | 备注 |
|----|---------|------|------|
| 微信搜一搜 | 2026-06-19 12:00 | ✅ healthy | - |
| 微信指数 | 2026-06-19 12:01 | ✅ healthy | - |
| PaiCoding | 2026-06-19 12:02 | ✅ healthy | - |
| 36 氪 | 2026-06-19 12:03 | ⚠️ slow | 响应 3.2s |
| 腾讯云 | 2026-06-19 11:00 | ❌ timeout | 待修复 |

健康检查结果写入 `references/data-source-health.log`。

---

## 6. 扩展数据源建议

待 v1.1 评估接入：
1. **新榜 (newrank.cn)** — 公众号真实阅读量、10w+ 检测
2. **清博 (gsdata.cn)** — 微信生态传播分析
3. **西瓜助手** — 视频号创作者数据
4. **百度指数 / Google Trends** — 时序对比
5. **GitHub Trending + Hugging Face Spaces** — 框架层开发者热度

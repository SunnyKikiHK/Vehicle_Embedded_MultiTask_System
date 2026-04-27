# Info Query Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 354 | Ask_Where | 当前位置查询 |
| 226 | Ask_Weekday | 查询星期 |
| 324 | Ask_Date | 查看日期 |
| 91 | Open_Weather | 打开天气 |
| 26 | Ask_Air_Condition | 查询空气 |
| 66 | Ask_Humidity | 查询湿度 |
| 209 | Query_UV_Level | 查询紫外线 |

## Shared Slot Type Definitions

### location
```
resolution: Always current GPS location. No default fallback — always query live GPS.
agents: Info Query Agent, Weather & Life Agent, Navigation Agent, Group Travel Agent
```

### date
```
resolution: Always "now". No date offset or historical query support in Info Query Agent.
agents: Info Query Agent, Weather & Life Agent
```

## Air Quality Grades

| AQI Range | Grade | Color | Description |
|-----------|-------|-------|-------------|
| 0-50 | 优 | Green | Excellent, no restrictions |
| 51-100 | 良 | Yellow | Good, suitable for outdoor |
| 101-150 | 轻度污染 | Orange | Sensitive groups should reduce outdoor activity |
| 151-200 | 中度污染 | Red | Everyone should reduce outdoor exertion |
| 201-300 | 重度污染 | Purple | Avoid outdoor activities |
| 300+ | 严重污染 | Maroon | Health warning of emergency conditions |

## Humidity Comfort Levels

| Humidity Range | Feeling |
|---------------|---------|
| 30-60% | Comfortable |
| < 30% | Dry — consider using humidifier |
| 60-80% | Slightly humid |
| > 80% | Humid — may feel muggy |

## UV Index Levels

| UV Index | Level | Protection Recommendation |
|----------|-------|------------------------|
| 0-2 | Low | No protection needed |
| 3-5 | Moderate | Wear sunglasses, use SPF 30+ |
| 6-7 | High | Reduce sun exposure 10am-4pm |
| 8-10 | Very High | Extra protection needed |
| 11+ | Extreme | Avoid sun exposure |

## Monitoring & Retraining

### Logging
- All API requests are logged in `news_api.log`
- Logged fields: query, timestamp, result categories

### Metrics
Run:
        python src/metrics.py


To view:
- Top search queries
- Daily usage volume

### Retraining
Run:
        python src/retrain_index.py


Recommended frequency:
- Daily for news-heavy systems
- Weekly minimum

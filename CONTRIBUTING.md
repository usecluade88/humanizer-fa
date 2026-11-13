# Contributing / مشارکت

برای گزارش مشکل، ورودی کوتاه، هدف، لحن و محدودیت‌های خواسته‌شده، خروجی واقعی و دلیل مشکل را ثبت کنید. اطلاعات مشتری، کلید، سفارش واقعی و دادهٔ شخصی را با نمونهٔ فرضی عوض کنید. متن خوب و بدون تغییر هم یک نتیجهٔ معتبر است.

Submit a small, non-private reproduction: request, source, requested tone/constraints, actual output, and the specific meaning or usability failure. Include the actual model/host settings if known; do not guess them.

## تغییر قواعد

یک خطای واقعی را با حداقل تغییر مؤثر اصلاح کنید. یک واژهٔ نامطلوب را به ممنوعیت همیشگی برای همهٔ سبک‌ها تبدیل نکنید. برای هر اصلاح، موردی به corpus یا آزمون ابزار مربوط اضافه کنید و موارد حفظ معنا و لحن‌های دیگر را دوباره بررسی کنید. خروجی مدل را به‌عنوان جواب طلایی واحد تثبیت نکنید؛ اطلاعات و هدف معیارند.

For rule changes, add a targeted regression case and run the applicable existing checks. Avoid turning one preference into a universal ban. Keep example outputs illustrative, not exact-output assertions for subjective prose. Tool tests should catch observable failures rather than merely match implementation wording.

## چک‌های محلی

```text
python scripts/validate_package.py
python -m unittest discover -s tests -v
```

برای ارزیابی مدل، روش و محدودیت‌ها را در کنار خروجی‌ها ثبت کنید. تعداد تست، امتیاز آشکارساز یا ترجیح یک داور را به ادعای «کاملاً انسانی» یا «بهترین» تبدیل نکنید.

Do not submit model API keys or live customer data. Report whether a result is a structural check, a language-task run, an independent model review or a human-editor judgment. Include appropriate attribution if adding third-party content.

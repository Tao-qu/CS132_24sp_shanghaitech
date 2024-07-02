# Project3 Painkiller Injection System 
## Consultation 1 Summary
Requirement: Panxin Tao 2022533112

Development: Zhekai Zhang 2022533057

Validation: Runkang Yang 2022533080

Date: 2024.4.8

---

## Summary

> - Q: Does 'total amount per day' mean 'per 24 hours'?
> - Q: When does the painkiller injection system work? Does it work all the day? If yes, does the $baseline \times time$ exceed the total amount per day. If no, do we need an interface for physician to set the injection period?
> 
> A: The two limits are 3ml every 24 hours and 1ml every one hour. When the limits are not reach, the injector will continue to inject.

> - Q: Obviously, the baseline is set by the physician. Then what about the bolus?
> 
> A: It's also set by the physician.

# worker_system

* Worker System is the Django Project holds the complete data setup.

## Store

* This is the application which handles all the business logics

* store/views.py holds all the 3 API's
  - GetRecentItem
  - GetBrandCount
  - GetItemsbyColor
 
**Note : Please add the required paramter in the params options**

* GetRecentItem - This API returns the latest record for the given date

```
 - API : /store/recent_items/
 - Required Parameter : {'date':'2017-10-01'}
 - Method : GET
```

* GetBrandCount - This API rturns the count of each brand in descending order for the given date

```
 - API : /store/brand_count/
 - Required Parameter : {'date':'2017-10-01'}
 - Method : GET
```

* GetItemsbyColor - This API rturns the latest 10 records for the given color

```
 - API : /store/color-items/
 - Required Parameter : {'color':'Black'}
 - Method : GET
```

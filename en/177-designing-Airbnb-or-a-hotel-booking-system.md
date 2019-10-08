---
layout: post
title: "Designing Airbnb or a hotel booking system"
date: 2019-10-06 01:39
comments: true
slides: false
categories: system design
language: en
abstract: For guests and hosts, we store data with a relational database and build indexes to search by location, metadata, and availability. We can use external vendors for payment and remind the reservations with a priority queue.
references:
  - https://www.vertabelo.com/blog/designing-a-data-model-for-a-hotel-room-booking-system/
---

## Requirements
* for guests
    * search rooms by locations, dates, number of rooms, and number of guests
    * get room details (like picture, name, review, address, etc.) and prices
    * pay and book room from inventory by date and room id
        * checkout as a guest 
        * user is logged in already
    * notification via Email and mobile push notification
* for hotel or rental administrators (suppliers/hosts)
    * administrators (receptionist/manager/rental owner): manage room inventory and help the guest to check-in and check out
    * housekeeper: clean up rooms routinely

## Architecture

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1570439920/web-guiguio/hotel-booking-system_2.png)

## Components

### Inventory <> Bookings <> Users (guests and hosts)

Suppliers provide their room details in the inventory. And users can search, get, and reserve rooms accordingly. After reserving the room, the user's payment will change the `status` of the `reserved_room` as well. You could check the data model in [this post](https://www.vertabelo.com/blog/designing-a-data-model-for-a-hotel-room-booking-system/).

### How to find available rooms?

* by location: geo-search with [spatial indexing](https://en.wikipedia.org/wiki/Spatial_database), e.g. geo-hash or quad-tree.
* by room metadata: apply filters or search conditions when querying the database.
* by date-in and date-out and availability. Two options:
    * option 1: for a given `room_id`, check all `occupied_room` today or later, transform the data structure to an array of occupation by days, and finally find available slots in the array. This process might be time-consuming, so we can build the availability index.
    * option 2: for a given `room_id`, always create an entry for an occupied day. Then it will be easier to query unavailable slots by dates. 

### For hotels, syncing data

If it is a hotel booking system, then it will probably publish to Booking Channels like GDS, Aggregators, and Wholesalers. 

![Hotel Booking Ecosystem](https://res.cloudinary.com/dohtidfqh/image/upload/v1570439485/web-guiguio/scheme.png)

To sync data across those places. We can 

1. [retry with idempotency to improve the success rate of the external calls and ensure no duplicate orders](https://puncsky.com/notes/43-how-to-design-robust-and-predictable-apis-with-idempotency).
2. provide webhook callback APIs to external vendors to update status in the internal system.

### Payment & Bookkeeping

Data model: [double-entry bookkeeping](https://puncsky.com/notes/167-designing-paypal-money-transfer#payment-service)

To execute the payment, since we are calling the external payment gateway, like bank or Stripe, Braintree, etc. It is crucial to keep data in-sync across different places. [We need to sync data across the transaction table and external banks and vendors.](https://puncsky.com/#how-to-sync-across-the-transaction-table-and-external-banks-and-vendors)

### Notifier for reminders / alerts

The notification system is essentially a delayer scheduler (priority queue + subscriber) plus API integrations.

For example, a daily cronjob will query the database for notifications to be sent out today and put them into the priority queue by date. The subscriber will get the earliest ones from the priority queue and send out if reaching the expected timestamp. Otherwise, put the task back to the queue and sleep to make the CPU idle for other work, which can be interrupted if there are new alerts added for today.

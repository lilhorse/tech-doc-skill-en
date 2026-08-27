# Getting Started With The Consignment API.

The Consignment API lets you organize consignments and synchronize them with your
courier's systems. As of this writing, the sandbox does not support bulk operations.

Please note that requests are rate-limited to 50 percent of your organization's quota.
Each consignment is analyzed by the routing engine before it is dispatched – see the
3rd column of the table for the behavior of each service level.

You can customize the label color and the dispatch center. Every request must be
authorized with a license key, e.g. `Authorization: Bearer <key>`. Labels are modeled
on the courier's catalog and can be canceled and/or amended.

## Configuring A Consignment

1. Uncheck Automatically synchronize.
2. Please click Save.
3. Set this to true.

For details, click here.

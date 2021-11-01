# Quantitative Bridge Library

With this package one can analyze his/her play in the **Hungarian Championship** or where the same online commentation is used. This tool provides analyzer where the achieved score and playing can be compared to the field result, or to the theoretical optimum ([double dummy](https://www.fgbradleys.com/rules//Double%20Dummy%20Bridge.pdf)).

The `project/base` folder contains all the necessary libraries which need for a basic play with seating, bidding, and playing a pre-defined or randomly shuffered board. The `project/analytics` provides an interface with the online commentator program and containes a double dummy solver.

:warning: **Do not** forgot to build the DDS package before use it, for installation steps reach the [manual](https://github.com/antsticky/BridgeLib/tree/main/project/analytics/dds_project)

## Examples
For this repository a few examples are attached, see [Examples](https://github.com/antsticky/BridgeLib/tree/main/examples).


## Links
-  **Linus Hein**'s double dummy solver - [C++ implementation](http://privat.bahnhof.se/wb758135/)
- **Bo Haglund**'s and **Soren Hein**'s python interface for the double dummy solver -[Python Interface](https://github.com/dds-bridge/dds)

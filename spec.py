# [Balsa]
balsaSpec = {
    "PowerSupplySpec":
    {
        "Current":
        {
            "High": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 },
            "Low": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 }},

        "Voltage":
        {
            "High": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 },
            "Low": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 }}},

    "EloadSpec":
    {
        "Current":
        {
            "High": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 },
            "Mid": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 },
            "Low": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 }},

        "Voltage":
        {
            "High": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 },
            "Mid": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 },
            "Low": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 }},
        "Power":
        {
            "High": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 },
            "Mid": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 },
            "Low": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 }},

        "Resistance":
        {
            "High": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 },
            "Mid": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 },
            "Low": {
                "Gain"      :   0.00001,
                "Offset"    :   0.0001 }}}}

x = (balsaSpec["PowerSupplySpec"]["Current"]["High"]["Gain"])

// Bike Sales Power Query M
// Option A: update ExcelWorkbookPath to the local path of "Excel Project Dataset.xlsx".
// Option B: use the generated CSV in powerbi_output/data/bike_buyers_clean.csv and skip this query.

let
    ExcelWorkbookPath = "C:\Path\To\Excel Project Dataset.xlsx",
    Source = Excel.Workbook(File.Contents(ExcelWorkbookPath), null, true),
    RawSheet = Source{[Item="bike_buyers", Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(RawSheet, [PromoteAllScalars=true]),
    TypedColumns = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"ID", Int64.Type},
            {"Marital Status", type text},
            {"Gender", type text},
            {"Income", Int64.Type},
            {"Children", Int64.Type},
            {"Education", type text},
            {"Occupation", type text},
            {"Home Owner", type text},
            {"Cars", Int64.Type},
            {"Commute Distance", type text},
            {"Region", type text},
            {"Age", Int64.Type},
            {"Purchased Bike", type text}
        }
    ),
    ExpandedMaritalStatus = Table.ReplaceValue(TypedColumns, "M", "Married", Replacer.ReplaceText, {"Marital Status"}),
    ExpandedMaritalStatus2 = Table.ReplaceValue(ExpandedMaritalStatus, "S", "Single", Replacer.ReplaceText, {"Marital Status"}),
    ExpandedGender = Table.ReplaceValue(ExpandedMaritalStatus2, "F", "Female", Replacer.ReplaceText, {"Gender"}),
    ExpandedGender2 = Table.ReplaceValue(ExpandedGender, "M", "Male", Replacer.ReplaceText, {"Gender"}),
    RemovedDuplicates = Table.Distinct(ExpandedGender2, {"ID"}),
    AddedAgeBracket = Table.AddColumn(
        RemovedDuplicates,
        "Age Bracket",
        each if [Age] < 31 then "Adult" else if [Age] <= 54 then "Middle Age" else "Old",
        type text
    ),
    AddedAgeBracketSort = Table.AddColumn(
        AddedAgeBracket,
        "Age Bracket Sort",
        each if [Age Bracket] = "Adult" then 1 else if [Age Bracket] = "Middle Age" then 2 else 3,
        Int64.Type
    ),
    AddedCommuteSort = Table.AddColumn(
        AddedAgeBracketSort,
        "Commute Distance Sort",
        each
            if [Commute Distance] = "0-1 Miles" then 1
            else if [Commute Distance] = "1-2 Miles" then 2
            else if [Commute Distance] = "2-5 Miles" then 3
            else if [Commute Distance] = "5-10 Miles" then 4
            else 5,
        Int64.Type
    ),
    AddedIncomeBand = Table.AddColumn(
        AddedCommuteSort,
        "Income Band",
        each
            if [Income] < 40000 then "Under $40k"
            else if [Income] < 60000 then "$40k-$59k"
            else if [Income] < 80000 then "$60k-$79k"
            else if [Income] < 100000 then "$80k-$99k"
            else "$100k+",
        type text
    ),
    AddedIncomeBandSort = Table.AddColumn(
        AddedIncomeBand,
        "Income Band Sort",
        each
            if [Income Band] = "Under $40k" then 1
            else if [Income Band] = "$40k-$59k" then 2
            else if [Income Band] = "$60k-$79k" then 3
            else if [Income Band] = "$80k-$99k" then 4
            else 5,
        Int64.Type
    ),
    AddedPurchaseFlag = Table.AddColumn(
        AddedIncomeBandSort,
        "Purchase Flag",
        each if [Purchased Bike] = "Yes" then 1 else 0,
        Int64.Type
    ),
    RenamedID = Table.RenameColumns(AddedPurchaseFlag, {{"ID", "Customer ID"}}),
    ReorderedColumns = Table.ReorderColumns(
        RenamedID,
        {
            "Customer ID", "Marital Status", "Gender", "Income", "Income Band", "Income Band Sort",
            "Children", "Education", "Occupation", "Home Owner", "Cars", "Commute Distance",
            "Commute Distance Sort", "Region", "Age", "Age Bracket", "Age Bracket Sort",
            "Purchased Bike", "Purchase Flag"
        }
    )
in
    ReorderedColumns

open System.IO

let inputFile = "input1.txt"

let (arr1, arr2) = File.ReadAllLines(inputFile)
                |> Array.map  _.Split("   ")
                |> Array.map (fun arr -> arr |> Array.map int)
                |> Array.map (fun arr -> (arr.[0], arr.[1]))
                |> Array.unzip

let s_arr1 = Array.sort(arr1)
let s_arr2 = Array.sort(arr2)

let sol1 = Array.zip s_arr1 s_arr2
            |> Array.map (fun (a, b) -> abs(a - b))
            |> Array.sum
printfn "Solution 1: %A" sol1

let cnt2 = arr2 |> Seq.countBy id |> Map
let sol2 = arr1
        |> Array.map (fun a ->  match cnt2.TryFind a with
                                                | Some x -> x * a
                                                | None -> 0
                    )
        |> Array.sum

printfn "Solution 2: %A" sol2

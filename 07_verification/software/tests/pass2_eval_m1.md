# eval_m1.py output

```json
{
 "model_version": "m1-effb0-0.1-provisional",
 "classes": [
  "unripe",
  "underripe",
  "ripe",
  "overripe"
 ],
 "counts": {
  "test": {
   "unripe": 34,
   "underripe": 0,
   "ripe": 41,
   "overripe": 14
  },
  "train": {
   "unripe": 40,
   "underripe": 0,
   "ripe": 123,
   "overripe": 60
  }
 },
 "mapping_check": {
  "class_mismatches": [],
  "n_class_mismatches": 0,
  "split_mismatches": [],
  "n_split_mismatches": 0,
  "D1_names": {
   "Immature": "unripe",
   "Partially Ripe": "underripe",
   "Fully Ripe": "ripe",
   "Overripe": "overripe",
   "Decayed": "overripe",
   "Unripe": "unripe",
   "Mature": "ripe",
   "Underripe": "underripe"
  }
 },
 "A_serving_no_exif": {
  "n": 89,
  "accuracy": 0.8989,
  "macro_f1_present_classes": 0.9162,
  "per_class": {
   "unripe": {
    "precision": 1.0,
    "recall": 0.735,
    "f1": 0.847,
    "n": 34
   },
   "ripe": {
    "precision": 0.82,
    "recall": 1.0,
    "f1": 0.901,
    "n": 41
   },
   "overripe": {
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0,
    "n": 14
   }
  },
  "cm": [
   [
    25,
    0,
    9,
    0
   ],
   [
    0,
    0,
    0,
    0
   ],
   [
    0,
    0,
    41,
    0
   ],
   [
    0,
    0,
    0,
    14
   ]
  ],
  "onnx_latency_ms_p50": 11.9,
  "cam_mass_in_centre_mean": 0.823,
  "dedup_test": {
   "n": 83,
   "accuracy": 0.8916,
   "macro_f1_present_classes": 0.9112,
   "cm": [
    [
     24,
     0,
     9,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     37,
     0
    ],
    [
     0,
     0,
     0,
     13
    ]
   ]
  },
  "errors": [
   [
    "FFBtest/TestUnripe/TestUnripe(14).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(18).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(2).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(21).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(22).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(32).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(33).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(7).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(9).jpg",
    "unripe",
    "ripe"
   ]
  ]
 },
 "B_training_exif": {
  "n": 89,
  "accuracy": 0.8989,
  "macro_f1_present_classes": 0.9162,
  "per_class": {
   "unripe": {
    "precision": 1.0,
    "recall": 0.735,
    "f1": 0.847,
    "n": 34
   },
   "ripe": {
    "precision": 0.82,
    "recall": 1.0,
    "f1": 0.901,
    "n": 41
   },
   "overripe": {
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0,
    "n": 14
   }
  },
  "cm": [
   [
    25,
    0,
    9,
    0
   ],
   [
    0,
    0,
    0,
    0
   ],
   [
    0,
    0,
    41,
    0
   ],
   [
    0,
    0,
    0,
    14
   ]
  ],
  "onnx_latency_ms_p50": 13.7,
  "cam_mass_in_centre_mean": 0.823,
  "dedup_test": {
   "n": 83,
   "accuracy": 0.8916,
   "macro_f1_present_classes": 0.9112,
   "cm": [
    [
     24,
     0,
     9,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     37,
     0
    ],
    [
     0,
     0,
     0,
     13
    ]
   ]
  },
  "errors": [
   [
    "FFBtest/TestUnripe/TestUnripe(14).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(18).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(2).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(21).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(22).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(32).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(33).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(7).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(9).jpg",
    "unripe",
    "ripe"
   ]
  ]
 },
 "exif_rotated_test_images": 50,
 "reported": {
  "n": 89,
  "accuracy": 0.9326,
  "macro_f1_present_classes": 0.9371,
  "within_one_class_accuracy": 0.9326,
  "per_class": {
   "unripe": {
    "precision": 1.0,
    "recall": 0.824,
    "f1": 0.903,
    "n": 34
   },
   "ripe": {
    "precision": 0.891,
    "recall": 1.0,
    "f1": 0.943,
    "n": 41
   },
   "overripe": {
    "precision": 0.933,
    "recall": 1.0,
    "f1": 0.966,
    "n": 14
   }
  },
  "confusion_matrix": {
   "labels": [
    "unripe",
    "underripe",
    "ripe",
    "overripe"
   ],
   "rows_true_cols_pred": [
    [
     28,
     0,
     5,
     1
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     41,
     0
    ],
    [
     0,
     0,
     0,
     14
    ]
   ]
  }
 },
 "leakage": {
  "exact_md5_pairs": [
   [
    "FFBtest/TestRipe/TestRipe(15).jpg",
    "FFBtrain/TrainRipe/TrainRipe(107).jpg"
   ]
  ],
  "near_dup_pairs_hamming_le6": [
   [
    "FFBtest/TestOverripe/TestOverripe(11).jpg",
    "FFBtrain/TrainOverripe/TrainOverripe(39).jpg",
    0
   ],
   [
    "FFBtest/TestRipe/TestRipe(15).jpg",
    "FFBtrain/TrainRipe/TrainRipe(107).jpg",
    0
   ],
   [
    "FFBtest/TestRipe/TestRipe(16).JPG",
    "FFBtrain/TrainRipe/TrainRipe(20).JPG",
    4
   ],
   [
    "FFBtest/TestRipe/TestRipe(39).JPG",
    "FFBtrain/TrainRipe/TrainRipe(20).JPG",
    3
   ],
   [
    "FFBtest/TestRipe/TestRipe(9).jpg",
    "FFBtrain/TrainRipe/TrainRipe(133).jpg",
    1
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(15).jpg",
    "FFBtrain/TrainUnripe/TrainUnripe(101).jpg",
    0
   ]
  ],
  "n_exact": 1,
  "n_near": 6
 }
}
```

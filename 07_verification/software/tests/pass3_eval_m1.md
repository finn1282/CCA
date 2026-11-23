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
 "A_legacy_serving_no_exif": {
  "n": 89,
  "accuracy": 0.9213,
  "macro_f1_present_classes": 0.9355,
  "per_class": {
   "unripe": {
    "precision": 1.0,
    "recall": 0.794,
    "f1": 0.885,
    "n": 34
   },
   "ripe": {
    "precision": 0.854,
    "recall": 1.0,
    "f1": 0.921,
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
    27,
    0,
    7,
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
  "onnx_latency_ms_p50": 15.9,
  "cam_mass_in_centre_mean": 0.81,
  "owner_dedup_test": {
   "n": 81,
   "accuracy": 0.9136,
   "macro_f1_present_classes": 0.9295,
   "cm": [
    [
     25,
     0,
     7,
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
     36,
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
  "dedup_test": {
   "n": 83,
   "accuracy": 0.9157,
   "macro_f1_present_classes": 0.9316,
   "cm": [
    [
     26,
     0,
     7,
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
   ]
  ]
 },
 "B_legacy_exif": {
  "n": 89,
  "accuracy": 0.9101,
  "macro_f1_present_classes": 0.9259,
  "per_class": {
   "unripe": {
    "precision": 1.0,
    "recall": 0.765,
    "f1": 0.867,
    "n": 34
   },
   "ripe": {
    "precision": 0.837,
    "recall": 1.0,
    "f1": 0.911,
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
    26,
    0,
    8,
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
  "onnx_latency_ms_p50": 15.8,
  "cam_mass_in_centre_mean": 0.812,
  "owner_dedup_test": {
   "n": 81,
   "accuracy": 0.9012,
   "macro_f1_present_classes": 0.919,
   "cm": [
    [
     24,
     0,
     8,
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
     36,
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
  "dedup_test": {
   "n": 83,
   "accuracy": 0.9036,
   "macro_f1_present_classes": 0.9215,
   "cm": [
    [
     25,
     0,
     8,
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
    "FFBtest/TestUnripe/TestUnripe(9).jpg",
    "unripe",
    "ripe"
   ]
  ]
 },
 "C_shared_serving_path": {
  "n": 89,
  "accuracy": 0.9213,
  "macro_f1_present_classes": 0.9275,
  "per_class": {
   "unripe": {
    "precision": 1.0,
    "recall": 0.794,
    "f1": 0.885,
    "n": 34
   },
   "ripe": {
    "precision": 0.872,
    "recall": 1.0,
    "f1": 0.932,
    "n": 41
   },
   "overripe": {
    "precision": 0.933,
    "recall": 1.0,
    "f1": 0.966,
    "n": 14
   }
  },
  "cm": [
   [
    27,
    0,
    6,
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
  ],
  "onnx_latency_ms_p50": 14.7,
  "cam_mass_in_centre_mean": 0.8,
  "owner_dedup_test": {
   "n": 81,
   "accuracy": 0.9136,
   "macro_f1_present_classes": 0.9211,
   "cm": [
    [
     25,
     0,
     6,
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
     36,
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
  "dedup_test": {
   "n": 83,
   "accuracy": 0.9157,
   "macro_f1_present_classes": 0.9231,
   "cm": [
    [
     26,
     0,
     6,
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
    "overripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(18).jpg",
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
    "FFBtest/TestUnripe/TestUnripe(27).jpg",
    "unripe",
    "ripe"
   ],
   [
    "FFBtest/TestUnripe/TestUnripe(33).jpg",
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
  "n": 81,
  "accuracy": 0.9136,
  "macro_f1_present_classes": 0.9211,
  "within_one_class_accuracy": 0.9136,
  "per_class": {
   "unripe": {
    "precision": 1.0,
    "recall": 0.781,
    "f1": 0.877,
    "n": 32
   },
   "ripe": {
    "precision": 0.857,
    "recall": 1.0,
    "f1": 0.923,
    "n": 36
   },
   "overripe": {
    "precision": 0.929,
    "recall": 1.0,
    "f1": 0.963,
    "n": 13
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
     25,
     0,
     6,
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
     36,
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
  "_dropped": [
   {
    "test": "TestOverripe/TestOverripe(11).jpg",
    "train_twin": "TrainOverripe/TrainOverripe(39).jpg",
    "hamming": 0
   },
   {
    "test": "TestRipe/TestRipe(15).jpg",
    "train_twin": "TrainRipe/TrainRipe(107).jpg",
    "hamming": 0
   },
   {
    "test": "TestRipe/TestRipe(16).JPG",
    "train_twin": "TrainRipe/TrainRipe(19).JPG",
    "hamming": 5
   },
   {
    "test": "TestRipe/TestRipe(18).jpg",
    "train_twin": "TrainRipe/TrainRipe(34).jpg",
    "hamming": 5
   },
   {
    "test": "TestRipe/TestRipe(39).JPG",
    "train_twin": "TrainRipe/TrainRipe(18).JPG",
    "hamming": 6
   },
   {
    "test": "TestRipe/TestRipe(9).jpg",
    "train_twin": "TrainRipe/TrainRipe(133).jpg",
    "hamming": 5
   },
   {
    "test": "TestUnripe/TestUnripe(15).jpg",
    "train_twin": "TrainUnripe/TrainUnripe(101).jpg",
    "hamming": 1
   },
   {
    "test": "TestUnripe/TestUnripe(8).jpg",
    "train_twin": "TrainUnripe/TrainUnripe(98).jpg",
    "hamming": 2
   }
  ]
 },
 "reported_serving_path": {
  "n": 81,
  "accuracy": 0.9136,
  "macro_f1_present_classes": 0.9211,
  "within_one_class_accuracy": 0.9136,
  "per_class": {
   "unripe": {
    "precision": 1.0,
    "recall": 0.781,
    "f1": 0.877,
    "n": 32
   },
   "ripe": {
    "precision": 0.857,
    "recall": 1.0,
    "f1": 0.923,
    "n": 36
   },
   "overripe": {
    "precision": 0.929,
    "recall": 1.0,
    "f1": 0.963,
    "n": 13
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
     25,
     0,
     6,
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
     36,
     0
    ],
    [
     0,
     0,
     0,
     13
    ]
   ]
  }
 },
 "owner_dedupe_covers_mine": {
  "covered": [
   "FFBtest/TestOverripe/TestOverripe(11).jpg",
   "FFBtest/TestRipe/TestRipe(15).jpg",
   "FFBtest/TestRipe/TestRipe(16).JPG",
   "FFBtest/TestRipe/TestRipe(39).JPG",
   "FFBtest/TestRipe/TestRipe(9).jpg",
   "FFBtest/TestUnripe/TestUnripe(15).jpg"
  ],
  "missing": [],
  "owner_extra": [
   "FFBtest/TestRipe/TestRipe(18).jpg",
   "FFBtest/TestUnripe/TestUnripe(8).jpg"
  ]
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

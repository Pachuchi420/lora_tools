#include <iostream>
#include <algorithm>
#include <vector>

// Swap function
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Median of five function
int medianOfFive(int array[], int n) {
    std::sort(array, array+n); // Sort the array
    return array[n/2]; // Return the median
}

// Median of Medians function
int medianOfMedians(int array[], int n) {
    int numMedians = n/5;
    std::vector<int> medians(numMedians);

    for (int i = 0; i < numMedians; i++) {
        medians[i] = medianOfFive(&array[i*5], 5);
    }

    if (numMedians <= 5) {
        return medianOfFive(&medians[0], numMedians);
    } else {
        return medianOfMedians(&medians[0], numMedians);
    }
}

// Partition function
int partition(int array[], int n, int pivot) {
    // Swap pivot with last element
    for (int i = 0; i < n; i++) {
        if (array[i] == pivot) {
            swap(&array[i], &array[n - 1]);
            break;
        }
    }

    int i = 0;
    for (int j = 0; j < n - 1; j++) {
        if (array[j] <= pivot) {
            swap(&array[i], &array[j]);
            i++;
        }
    }
    swap(&array[i], &array[n - 1]);

    return i;
}

// Quickselect function
int quickselect(int array[], int n, int k) {
    if (n == 1) {
        return array[0];
    }

    int pivot = medianOfMedians(array, n);
    int index = partition(array, n, pivot);

    if (k == index) {
        return array[index];
    } else if (k < index) {
        return quickselect(array, index, k);
    } else {
        return quickselect(array + index + 1, n - index - 1, k - index - 1);
    }
}

int main() {
    // Test quickselect function
    int array[10] = {10, 4, 5, 8, 6, 11, 26, 3, 1, 2};
    int n = sizeof(array) / sizeof(array[0]);
    int k = 5;  // Find the 6th smallest element
    int result = quickselect(array, n, k);
    std::cout << "6th smallest element is " << result;
    return 0;
}

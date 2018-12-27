<?php

$testPath = './datasets/images/cat_breeds/test/';
$trainPath = './datasets/images/cat_breeds/train/';
$fi = new FilesystemIterator($trainPath, FilesystemIterator::SKIP_DOTS);

foreach ($fi as $key => $fileInfo) {
    $fi2 = new FilesystemIterator($key, FilesystemIterator::KEY_AS_PATHNAME);
    $size = (int)(iterator_count($fi2) * 0.2) ;
    $count = 0;
    foreach ($fi2 as $subKey => $subFileInfo) {
        if ($count == $size) break;
        print "Will move " . $subKey . " to " . str_replace('/train/', '/test/', $subKey) . "\n";
        rename($subKey, str_replace('/train/', '/test/', $subKey));
        $count ++;
    }
    $fi2 = null;
}
$fi = null;
print "\n\n";

<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\App;

class DatabaseSeeder extends Seeder
{
    public function run()
    {
        if (App::environment('production')) {
            $this->call([
                ProductionSeeder::class,
            ]);
        } else {
            $this->call([
                UserSeeder::class,
                CaseManagementSeeder::class, // Run this before TestDataSeeder since it sets up reference data
                TestDataSeeder::class,
            ]);
        }
    }
}

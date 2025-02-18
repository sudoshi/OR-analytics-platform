<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;

class ProductionSeeder extends Seeder
{
    /**
    * Run the database seeds.
    * 
    * This seeder is designed to be safely run multiple times without duplicating or
    * destroying existing production data. Each seeder component will check for
    * existing data before proceeding.
    */
    public function run(): void
    {
        // Only seed users if none exist to prevent overwriting production data
        if (User::count() === 0) {
            $this->call([
                UserSeeder::class,
            ]);
        } else {
            $this->command->info('Skipping user seeding - existing users found');
        }

        // Add additional production seeders here with similar safety checks
    }
}


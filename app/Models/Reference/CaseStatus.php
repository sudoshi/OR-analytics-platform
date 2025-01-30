<?php

namespace App\Models\Reference;

use App\Models\ORCase;
use Illuminate\Database\Eloquent\Relations\HasMany;

class CaseStatus extends BaseReference
{
    public $timestamps = false;
    protected $table = 'prod.casestatus';
    protected $primaryKey = 'status_id';

    protected $fillable = [
        'name',
        'code',
        'active_status',
        'created_by',
        'modified_by',
        'created_date',
        'modified_date',
        'is_deleted'
    ];

    protected $casts = [
        'active_status' => 'boolean',
        'is_deleted' => 'boolean',
        'created_date' => 'datetime',
        'modified_date' => 'datetime'
    ];

    public function cases(): HasMany
    {
        return $this->hasMany(ORCase::class, 'status_id', 'status_id');
    }

    protected static function boot()
    {
        parent::boot();

        static::creating(function ($model) {
            $model->created_date = $model->freshTimestamp();
            $model->modified_date = $model->freshTimestamp();
        });

        static::updating(function ($model) {
            $model->modified_date = $model->freshTimestamp();
        });
    }
}

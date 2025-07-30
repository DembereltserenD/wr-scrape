import React, { useState } from 'react';
import { Button, Card, CardHeader, CardBody, CardFooter, Dropdown } from '../components/UI';
import type { DropdownOption } from '../components/UI';

const UIComponentsTest: React.FC = () => {
    const [dropdownValue, setDropdownValue] = useState('');
    const [loading, setLoading] = useState(false);

    const dropdownOptions: DropdownOption[] = [
        { value: 'strongest', label: 'Хамгийн хүчтэй' },
        { value: 'strong', label: 'Хүчтэй' },
        { value: 'good', label: 'Сайн' },
        { value: 'average', label: 'Дундаж' },
        { value: 'weak', label: 'Сул' }
    ];

    const handleLoadingTest = () => {
        setLoading(true);
        setTimeout(() => setLoading(false), 2000);
    };

    return (
        <div className="min-h-screen bg-background-dark p-8">
            <div className="max-w-6xl mx-auto space-y-8">
                <h1 className="text-4xl font-bold text-white mb-8">UI Components Test</h1>

                {/* Button Tests */}
                <Card variant="gaming" size="lg">
                    <CardHeader>
                        <h2 className="text-2xl font-bold text-white">Button Components</h2>
                    </CardHeader>
                    <CardBody>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {/* Primary Buttons */}
                            <div className="space-y-3">
                                <h3 className="text-lg font-semibold text-white">Primary Buttons</h3>
                                <Button variant="primary" size="sm">Small Primary</Button>
                                <Button variant="primary" size="md">Medium Primary</Button>
                                <Button variant="primary" size="lg">Large Primary</Button>
                                <Button variant="primary" size="xl">Extra Large</Button>
                            </div>

                            {/* Secondary Buttons */}
                            <div className="space-y-3">
                                <h3 className="text-lg font-semibold text-white">Secondary Buttons</h3>
                                <Button variant="secondary" size="sm">Small Secondary</Button>
                                <Button variant="secondary" size="md">Medium Secondary</Button>
                                <Button variant="secondary" size="lg">Large Secondary</Button>
                                <Button variant="secondary" size="xl">Extra Large</Button>
                            </div>

                            {/* Other Variants */}
                            <div className="space-y-3">
                                <h3 className="text-lg font-semibold text-white">Other Variants</h3>
                                <Button variant="outline">Outline Button</Button>
                                <Button variant="ghost">Ghost Button</Button>
                                <Button variant="danger">Danger Button</Button>
                                <Button disabled>Disabled Button</Button>
                            </div>
                        </div>

                        {/* Button with Icons and Loading */}
                        <div className="mt-6 space-y-3">
                            <h3 className="text-lg font-semibold text-white">Special Features</h3>
                            <div className="flex flex-wrap gap-3">
                                <Button
                                    variant="primary"
                                    leftIcon={
                                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                                        </svg>
                                    }
                                >
                                    With Left Icon
                                </Button>
                                <Button
                                    variant="secondary"
                                    rightIcon={
                                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                        </svg>
                                    }
                                >
                                    With Right Icon
                                </Button>
                                <Button
                                    variant="primary"
                                    loading={loading}
                                    onClick={handleLoadingTest}
                                >
                                    {loading ? 'Loading...' : 'Test Loading'}
                                </Button>
                                <Button variant="outline" fullWidth>Full Width Button</Button>
                            </div>
                        </div>
                    </CardBody>
                </Card>

                {/* Card Tests */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <Card variant="default" hoverable>
                        <CardHeader>
                            <h3 className="text-lg font-semibold text-white">Default Card</h3>
                        </CardHeader>
                        <CardBody>
                            <p className="text-gray-300">This is a default card with hover effect.</p>
                        </CardBody>
                        <CardFooter>
                            <Button variant="primary" size="sm">Action</Button>
                        </CardFooter>
                    </Card>

                    <Card variant="elevated" clickable>
                        <CardHeader>
                            <h3 className="text-lg font-semibold text-white">Elevated Card</h3>
                        </CardHeader>
                        <CardBody>
                            <p className="text-gray-300">This is an elevated card that's clickable.</p>
                        </CardBody>
                    </Card>

                    <Card variant="outlined" size="lg">
                        <CardHeader>
                            <h3 className="text-lg font-semibold text-white">Outlined Card</h3>
                        </CardHeader>
                        <CardBody>
                            <p className="text-gray-300">This is an outlined card with large size.</p>
                        </CardBody>
                    </Card>

                    <Card variant="gaming" hoverable>
                        <CardHeader>
                            <h3 className="text-lg font-semibold text-white">Gaming Card</h3>
                        </CardHeader>
                        <CardBody>
                            <p className="text-gray-300">This is a gaming-themed card with special effects.</p>
                        </CardBody>
                    </Card>
                </div>

                {/* Dropdown Tests */}
                <Card variant="gaming" size="lg">
                    <CardHeader>
                        <h2 className="text-2xl font-bold text-white">Dropdown Components</h2>
                    </CardHeader>
                    <CardBody>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {/* Default Dropdown */}
                            <div>
                                <h3 className="text-lg font-semibold text-white mb-3">Default Dropdown</h3>
                                <Dropdown
                                    options={dropdownOptions}
                                    value={dropdownValue}
                                    onChange={setDropdownValue}
                                    placeholder="Select tier..."
                                    label="Champion Tier"
                                />
                            </div>

                            {/* Gaming Dropdown */}
                            <div>
                                <h3 className="text-lg font-semibold text-white mb-3">Gaming Dropdown</h3>
                                <Dropdown
                                    variant="gaming"
                                    options={dropdownOptions}
                                    value={dropdownValue}
                                    onChange={setDropdownValue}
                                    placeholder="Select tier..."
                                    label="Champion Tier"
                                />
                            </div>

                            {/* Searchable Dropdown */}
                            <div>
                                <h3 className="text-lg font-semibold text-white mb-3">Searchable Dropdown</h3>
                                <Dropdown
                                    variant="gaming"
                                    searchable
                                    options={dropdownOptions}
                                    value={dropdownValue}
                                    onChange={setDropdownValue}
                                    placeholder="Search tiers..."
                                    label="Champion Tier"
                                />
                            </div>

                            {/* Different Sizes */}
                            <div>
                                <h3 className="text-lg font-semibold text-white mb-3">Small Size</h3>
                                <Dropdown
                                    size="sm"
                                    options={dropdownOptions}
                                    value={dropdownValue}
                                    onChange={setDropdownValue}
                                    placeholder="Small dropdown..."
                                />
                            </div>

                            <div>
                                <h3 className="text-lg font-semibold text-white mb-3">Large Size</h3>
                                <Dropdown
                                    size="lg"
                                    variant="gaming"
                                    options={dropdownOptions}
                                    value={dropdownValue}
                                    onChange={setDropdownValue}
                                    placeholder="Large dropdown..."
                                />
                            </div>

                            {/* Disabled and Error States */}
                            <div>
                                <h3 className="text-lg font-semibold text-white mb-3">States</h3>
                                <div className="space-y-3">
                                    <Dropdown
                                        disabled
                                        options={dropdownOptions}
                                        value=""
                                        onChange={() => { }}
                                        placeholder="Disabled dropdown..."
                                    />
                                    <Dropdown
                                        options={dropdownOptions}
                                        value=""
                                        onChange={() => { }}
                                        placeholder="Error state..."
                                        error="This field is required"
                                        required
                                    />
                                </div>
                            </div>
                        </div>
                    </CardBody>
                </Card>

                {/* Loading Card Test */}
                <Card variant="gaming" loading>
                    <div>Loading content...</div>
                </Card>
            </div>
        </div>
    );
};

export default UIComponentsTest;